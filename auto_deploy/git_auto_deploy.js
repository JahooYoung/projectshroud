const http = require('http')
const createHandler = require('github-webhook-handler')

const handler = createHandler({
    path: '/git-push',
    secret: 'f8b67895daf32ce8fb52aad8d41c8293f42e90c3'
})

http.createServer(function (req, res) {
  handler(req, res, function (err) {
    res.statusCode = 404
    res.end('no such location')
  })
}).listen(8765)

handler.on('push', function (event) {
  console.log('Received a push event for %s to %s',
    event.payload.repository.name,
    event.payload.ref)
})