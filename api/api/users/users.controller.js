const { sign } = require("jsonwebtoken")
const database = require("./users.service")
const schemas = require("../../configs/schemas")
const config = require("../../configs/configs")

module.exports = {
  createUser: async (req, res) => {
    const body = req.body
    const validate = schemas.createUser_schema.validate(req.body)
    const ip = req.connection.remoteAddress
    
    if (validate.error){
      return res.status(200).json({
        success: 0,
        message: validate.error.details[0].message
      })
    }

    database.create(body, (err, results) => {
      if (err) {
        if (err.code == 'ER_DUP_ENTRY'){
          return res.status(200).json({
            success: 0,
            message: "An account with this username already exists"
          })
        }
        console.log(err)
        return res.status(200).json({
          success: 0,
          message: 1
        })
      }

      if (results){
        return res.status(200).json({
          success: 1,
          message: `Account ${body.username} has been created successfully`
        })
      }
    })
  },
  login: async (req, res) => {
    const body = req.body
    const validate = schemas.login_schema.validate(req.body)
    const ip = req.connection.remoteAddress

    if (validate.error){
      return res.status(200).json({
        success: 0,
        message: validate.error.details[0].message
      })
    }

    database.getuserbyusername(body, async (err, results) => {
      if (err) {
        console.log(err);
      }
      if (!results) {
        return await res.status(200).json({
          success: 0,
          message: "invalid username or password"
        });
      }
      if (body.password == results.password) {
        const jsontoken = sign({username: results.username, perm: results.perm }, config.jwt.encryptkey, {expiresIn: config.jwt.expire})
        return res.status(200).json({
          success: 1,
          message: {username: body.username, accesstoken: jsontoken}
        })
      }else {
        return res.status(200).json({
          success: 0,
          message: "invalid username or password"
        });
      }
    });
  },
  listusers: async (req, res) => {
    const body = req.body

    database.getallusername(async (err, results) => {
      if (err) {
        return res.status(200).json({
          success: 0,
          message: 88
        });
      }
      return res.status(200).json({
        success: 1,
        message: results
      });
    });
  },
  deleteuser: async (req, res) => {
    const body = req.body

    const validate = schemas.deleteUser_schema.validate(req.body)

    if (validate.error){
      return res.status(200).json({
        success: 0,
        message: validate.error.details[0].message
      })
    }

    database.deleteuserbyusername(body, async (err, results) => {
      if (err) {
        return await res.status(200).json({
          success: 0,
          message: 104
        });
      }
      return res.status(200).json({
        success: 1,
        message: `User ${body.username} has been deleted`
      });
    });
  }
}