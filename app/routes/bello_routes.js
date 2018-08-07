// routes/bello_routes.js
const math = require('mathjs');
module.exports = function(app, num) {

    app.get('/bello', (req, res) => {
        // You'll create your text here.
        var num1 = req.query.num1;
        var num2 = req.query.num2;
        var add = math.add(num1,num2);
        console.log(req.body)
        res.send(add.toString())
      });
};