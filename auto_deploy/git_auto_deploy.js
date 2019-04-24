const http = require('http')
const createHandler = require('github-webhook-handler')
const spawn = require('child_process').spawn

function run_cmd(cmd, args, callback) {
  var child = spawn(cmd, args);
  var resp = '';

  child.stderr.on('data', function(buffer) { resp += buffer.toString(); });
  child.stderr.on('end', function() { callback (resp) });
}

const handler = createHandler({
    path: '/github-push',
    secret: 'shroud'
})

http.createServer(function (req, res) {
  handler(req, res, function (err) {
    res.statusCode = 404
    res.end('no such location')
  })
}).listen(8765)

handler.on('error', function (err) {
  console.error('Error:', err.message)
})

handler.on('push', function (event) {
  console.log('Received a push event for %s to %s',
    event.payload.repository.name,
    event.payload.ref)
  if (event.payload.ref === 'refs/heads/site') {
    run_cmd('sh', ['./git_auto_deploy.sh'], text => console.log(text));
  }
})