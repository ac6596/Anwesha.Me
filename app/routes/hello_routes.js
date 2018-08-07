// routes/hello_routes.js
module.exports = function(app, txt) {

    app.post('/hello', (req, res) => {
        // You'll create your text here.
        res.send('Hello')
      });
};