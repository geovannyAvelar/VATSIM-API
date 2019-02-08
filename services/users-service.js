var redis = require("redis");

client = redis.createClient();
client.on("error", function (err) {
  console.log("Error " + err);
});

var service = {};

service.getAllKeys = () => {
    return new Promise((resolve, reject) => {
      client.keys("vatsim:*", (err, keys) => {
        if(err) {
            reject(err);
        } else {
            resolve(keys)
        }
      });
    });
};

service.getHash = (key) => {
    return new Promise((resolve, reject) => {
        client.hgetall(key, (err, replies) => {
            if(err) {
                reject(err);
            } else {
                resolve(replies)
            }
        });
    });
};

module.exports = service;

