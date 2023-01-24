const core = require("@actions/core");
const github = require("@actions/github");

try {
  const pythonVersions = core.getInput("python-versions");
  console.log(`Python versions: ${pythonVersions}`);
} catch (error) {
  core.setFailed(error.message);
}
