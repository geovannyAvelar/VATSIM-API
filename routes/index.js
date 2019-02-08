var express = require('express');
var usersService = require('../services/users-service')
var router = express.Router();

router.get('/online', function(req, res, next) {
  usersService.getAllKeys()
    .then(keys => {
      (async() => {
        let results = await Promise.all(
          keys.map((key) => { return usersService.getHash(key) })
        );

        res.json(results)
      })();
    })
    .catch(err => console.log(err))
});

module.exports = router;
