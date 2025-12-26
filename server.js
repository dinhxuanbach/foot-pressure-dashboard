const express = require("express");
const path = require("path");
const app = express();

const PORT = 8080;

// Phục vụ các file tĩnh (HTML, CSS, JS) trong thư mục hiện tại
app.use(express.static(__dirname));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(PORT, () => {
  console.log(`Giao diện Web đang chạy tại: http://localhost:${PORT}`);
});
