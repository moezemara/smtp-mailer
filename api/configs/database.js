const { createPool } = require("mysql")
const config = require('./configs')

const pool = createPool({
  port: 3306,
  host: "localhost",
  user: config.database.username,
  password: config.database.password,
  database: config.database.database
})


module.exports = pool;
