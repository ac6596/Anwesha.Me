// routes/index.js
const helloRoutes = require('./hello_routes');
const belloRoutes = require('./bello_routes');
module.exports = function(app, txt) {
  helloRoutes(app, txt);
  // Other route groups could go here, in the future
  belloRoutes(app, txt);
};





