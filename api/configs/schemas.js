const joi = require('joi');
const config = require('./configs')

const createUser_schema = joi.object({
  username: joi.required(),
  password: joi.required()
})

const login_schema = joi.object({
  username: joi.required(),
  password: joi.required()
})

const deleteUser_schema = joi.object({
  username: joi.required()
})

module.exports= {
  createUser_schema, login_schema, deleteUser_schema
}