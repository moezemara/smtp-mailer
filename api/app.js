const express = require("express")
const config = require('./configs/configs')
const usersRouter = require("./api/users/users.router")

const app = express()

app.use(express.json())
app.use(function(err, req, res, next) {
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    res.json({
      success: 0,
      message: 999
    })
  }
  next(err)
})

app.use("/api/users", usersRouter)

app.get("/api", (req, res) => {
  res.json({
    success: 1,
    message: "welcome"
  })
})

//var server = https.createServer(options, app)

app.listen(config.port, () => {
  console.log('\x1b[32m%s\x1b[0m', "server starting on port : " + config.port)
})