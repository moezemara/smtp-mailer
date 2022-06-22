const controller = require("./users.controller")
const router = require("express").Router()

router.post("/registration", controller.createUser)
router.post("/login", controller.login)
router.get("/listusers", controller.listusers)
router.post("/deleteuser", controller.deleteuser)

module.exports = router;
