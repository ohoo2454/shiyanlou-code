var http = require("http");
var fs = require("fs");

var server = http.createServer();

server.on("request", function(req, res) {
    var url = req.url;
    if (url === "/") {
        res.setHeader("Content-Type", "text/plain");
        fs.readFile("./index.html", function(err, data) {
            if (err) {
                res.end("文件读取失败，请稍后重试！");
            } else {
                res.writeHead(200, {
                    "Content-Type": "text/html",
                });
                res.end(data);
            }
        });
    } else if (url === "/register") {
        fs.readFile("./register.html", function(err, data) {
            if (err) {
                res.end("文件读取失败，请稍后重试！");
            } else {
                res.setHeader("Content-Type", "text/html");
                res.end(data);
            }
        });
    } else {
        res.end("<h1>404 Not Found.</h1>");
    }
});

server.listen(8080, function() {
    console.log("Server is running...");
});