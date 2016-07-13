var scanpkg = require("scanpkg"),
    fs = require('fs'),
    child_process = require("child_process");

scanpkg.new("debs", function(err, result) {
    if (err == scanpkg.noDirError)
        console.error("Folder is not found");

    if (err == scanpkg.emptyDirError)
        console.error("Folder is empty");

    // console.log(result);
    fs.writeFile("Packages", result, "utf8", function(err) {
        if (err) {
            return console.log(err);
        }

        if (fs.existsSync("Packages.bz2")) {
            fs.unlink("Packages.bz2", function(err) {
                return console.log(err);
            });
            console.log("Removed existing Packages.bz2");
        }

        child_process.spawnSync("bzip2", ["Packages"]);
        console.log("Finished making Packages.bz2");
    });
});
