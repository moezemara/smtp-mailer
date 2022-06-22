const pool = require("../../configs/database");

module.exports = {
  create: (data, callback) => {
    pool.query(
      `insert into users(username, password)
                values(?,?)`,
      [
        data.username,
        data.password,
      ],
      (error, results, fields) => {
        if (error){
          return callback(error)
        }
        return callback(null, results)
      }
    )
  },
  getuserbyusername: (data, callback) => {
    pool.query(
      `select * from users where username = ?`,
      [data.username],
      (error, results, fields) => {
        if (error) {
          return callback(error);
        }
        return callback(null, results[0]);
      }
    );
  },
  getallusername: (callback) => {
    pool.query(
      `select username from users`,
      (error, results, fields) => {
        if (error) {
          return callback(error);
        }
        return callback(null, results);
      }
    );
  },
  deleteuserbyusername: (data, callback) => {
    pool.query(
      `delete from users where username = ?`,
      [data.username],
      (error, results, fields) => {
        if (error) {
          return callback(error);
        }
        return callback(null, results[0]);
      }
    );
  }
}
