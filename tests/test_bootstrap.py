import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/mukidoc-init"
SCRIPT = SKILL / "scripts/init_mukidoc.py"
TEMPLATE = (SKILL / "assets/template/AGENTS.md").read_bytes()
VERSION = json.loads((SKILL / "assets/manifest.json").read_text())["protocol_version"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    if not root.exists():
        return {}
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


def versioned(version):
    return ("# Prior protocol\n\n<!-- MukiDoc protocol version: " + version
            + " -->\n\n项目附加规则：保留用户内容。\n").encode()


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="mukidoc-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / "项目 with spaces"

    def run_init(self, *options, script=SCRIPT, expected_code=0):
        result = subprocess.run([sys.executable, "-B", str(script), str(self.project), *options],
                                capture_output=True, text=True, cwd=self.base)
        self.assertEqual(result.returncode, expected_code, result.stderr + result.stdout)
        return json.loads(result.stdout)

    def write_agent(self, data):
        self.project.mkdir(parents=True, exist_ok=True)
        (self.project / "AGENTS.md").write_bytes(data)

    def test_initialization_has_fixed_skeleton_and_no_optional_documents(self):
        result = self.run_init()
        self.assertEqual(result["agent"]["state"], "missing")
        for name in ("README", "AGENTS"):
            self.assertTrue((self.project / (name + ".md")).is_file())
        for name in ("OVERVIEW", "PHILOSOPHY", "ARCHITECTURE", "ROADMAP", "DECISION", "DEVLOG", "TODO"):
            self.assertTrue((self.project / "mukidoc" / (name + ".md")).is_file())
        for directory in ("design", "system_design", "implementation",
                          "information/raw_materials", "information/external_information",
                          "information/investigations", "information/playground",
                          "evaluation/philosophy", "evaluation/design",
                          "evaluation/system_design", "evaluation/implementation"):
            self.assertTrue((self.project / "mukidoc" / directory / ".gitkeep").is_file())
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), TEMPLATE)
        self.assertFalse((self.project / "mukidoc/evaluation/mukicheck").exists())
        for name in ("DATA_MODEL.md", "RUNTIME.md", "TECH_STACK.md", "API.md"):
            self.assertEqual(list(self.project.rglob(name)), [])

    def test_repeat_run_preserves_bytes_and_modification_times(self):
        self.run_init()
        (self.project / "README.md").write_bytes(b"User README\r\n")
        (self.project / "mukidoc/TODO.md").write_bytes(b"")
        before = snapshot(self.project)
        result = self.run_init()
        self.assertEqual(snapshot(self.project), before)
        self.assertEqual(result["files_created"], [])
        self.assertEqual(result["directories_created"], [])
        self.assertEqual(result["agent"]["state"], "current")
        self.assertFalse(result["agent"]["needs_confirmation"])

    def test_partial_project_is_completed_without_rewriting_existing_knowledge(self):
        self.project.mkdir()
        (self.project / "README.md").write_text("A real existing project\n")
        (self.project / "src").mkdir()
        (self.project / "src/app.py").write_text("print('unchanged')\n")
        before = snapshot(self.project)
        self.run_init()
        after = snapshot(self.project)
        for path, value in before.items():
            self.assertEqual(after[path], value)
        self.assertTrue((self.project / "mukidoc/TODO.md").is_file())

    def test_preview_does_not_create_missing_target_or_parent(self):
        self.project = self.base / "not-yet-created" / "project"
        result = self.run_init("--dry-run")
        self.assertEqual(result["status"], "planned")
        self.assertTrue(result["files_created"])
        self.assertFalse(self.project.parent.exists())

    def test_all_existing_protocol_states_are_preserved_by_default(self):
        cases = [(versioned("0.0.99"), "older"),
                 (versioned(VERSION), "same_version_modified"),
                 (b"# Local instructions\n", "unversioned"),
                 (versioned("999.0.0"), "newer")]
        for data, state in cases:
            with self.subTest(state=state):
                self.write_agent(data)
                result = self.run_init()
                self.assertEqual(result["agent"]["state"], state)
                self.assertEqual((self.project / "AGENTS.md").read_bytes(), data)
                self.assertEqual(result["agent"]["needs_confirmation"], state != "newer")
                self.assertEqual(list(self.project.glob("AGENTS.md.bak.*")), [])

    def test_versions_are_compared_numerically(self):
        self.write_agent(versioned("0.10.0"))
        self.assertEqual(self.run_init()["agent"]["state"], "newer")

    def test_old_version_update_creates_exact_backup_and_preserves_other_files(self):
        self.run_init()
        old = versioned("0.0.99")
        self.write_agent(old)
        before = snapshot(self.project)
        result = self.run_init("--update-agent", "--expected-agent-sha256", digest(old))
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), TEMPLATE)
        backup = self.project / result["agent"]["backup"]
        self.assertEqual(backup.read_bytes(), old)
        for name, value in before.items():
            if name != "AGENTS.md":
                self.assertEqual(snapshot(self.project)[name], value)
        self.assertFalse(result["agent"]["needs_confirmation"])

    def test_unversioned_and_local_modified_replacement_require_explicit_flag(self):
        for original in (b"# Existing unversioned instructions\r\n", versioned(VERSION)):
            self.write_agent(original)
            result = self.run_init("--replace-agent", "--expected-agent-sha256", digest(original))
            self.assertEqual((self.project / result["agent"]["backup"]).read_bytes(), original)
            self.assertEqual((self.project / "AGENTS.md").read_bytes(), TEMPLATE)
        self.assertEqual(len(list(self.project.glob("AGENTS.md.bak.*"))), 2)

    def test_update_without_review_digest_refuses_before_writes(self):
        self.write_agent(versioned("0.0.1"))
        before = snapshot(self.project)
        self.run_init("--update-agent", expected_code=1)
        self.assertEqual(snapshot(self.project), before)
        self.assertFalse((self.project / "mukidoc").exists())

    def test_file_changed_after_review_is_not_replaced(self):
        old = versioned("0.0.1")
        self.write_agent(old + b"New instruction after review\n")
        before = snapshot(self.project)
        result = self.run_init("--update-agent", "--expected-agent-sha256", digest(old), expected_code=1)
        self.assertIn("changed since review", result["error"])
        self.assertEqual(snapshot(self.project), before)

    def test_future_protocol_cannot_be_downgraded(self):
        future = versioned("999.0.0")
        self.write_agent(future)
        before = snapshot(self.project)
        for flag in ("--update-agent", "--replace-agent"):
            result = self.run_init(flag, "--expected-agent-sha256", digest(future), expected_code=1)
            self.assertIn("downgrade", result["error"])
            self.assertEqual(snapshot(self.project), before)

    def test_update_flag_cannot_overwrite_an_unversioned_file(self):
        original = b"# Project instructions\n"
        self.write_agent(original)
        self.run_init("--update-agent", "--expected-agent-sha256", digest(original), expected_code=1)
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), original)
        self.assertFalse((self.project / "mukidoc").exists())

    def test_preview_of_approved_update_does_not_write_backup(self):
        old = versioned("0.0.1")
        self.write_agent(old)
        before = snapshot(self.project)
        result = self.run_init("--dry-run", "--update-agent", "--expected-agent-sha256", digest(old))
        self.assertEqual(result["agent"]["action"], "replace")
        self.assertIsNone(result["agent"]["backup"])
        self.assertEqual(snapshot(self.project), before)

    def test_conflicting_directory_blocks_all_creation(self):
        self.project.mkdir()
        (self.project / "mukidoc").write_text("This is not a directory\n")
        before = snapshot(self.project)
        self.run_init(expected_code=1)
        self.assertEqual(snapshot(self.project), before)
        self.assertFalse((self.project / "README.md").exists())

    def test_managed_symlink_is_not_followed(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.project.mkdir()
        (self.project / "mukidoc").symlink_to(outside, target_is_directory=True)
        result = self.run_init(expected_code=1)
        self.assertIn("symlink", result["error"])
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_skill_runs_as_a_detached_copy(self):
        detached = self.base / "detached skill"
        shutil.copytree(SKILL, detached)
        result = self.run_init(script=detached / "scripts/init_mukidoc.py")
        self.assertEqual(result["status"], "initialized")
        self.assertEqual((self.project / "AGENTS.md").read_bytes(), TEMPLATE)

    def test_corrupt_bundle_refuses_before_creating_target(self):
        detached = self.base / "damaged skill"
        shutil.copytree(SKILL, detached)
        (detached / "assets/template/mukidoc/TODO.md").write_text("Corrupted template")
        result = self.run_init(script=detached / "scripts/init_mukidoc.py", expected_code=1)
        self.assertIn("checksum mismatch", result["error"])
        self.assertFalse(self.project.exists())

    def test_release_export_check_matches_canonical_protocol(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/sync_skill_assets.py"), "--check"],
                                capture_output=True, text=True, cwd=self.base)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
