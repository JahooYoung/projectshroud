const http = require('http')
const createHandler = require('github-webhook-handler')
const spawn = require('child_process').spawn

function run_cmd(cmd, args, callback) {
  const child = spawn(cmd, args)
  let resp = ''
  let finished = 0

  child.stderr.on('data', buffer => resp += buffer.toString())
  child.stdout.on('data', buffer => resp += buffer.toString())
  child.stderr.on('end', () => {
    if (++finished === 2) {
      callback(resp)
    }
  })
  child.stdout.on('end', () => {
    if (++finished === 2) {
      callback(resp)
    }
  })
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
  if (event.payload.ref !== 'refs/heads/site') {
    return
  }
  let frontendUpdated = false
  ['added', 'removed', 'modified'].forEach(ele => {
    event.payload.commits[ele].forEach(file => {
      if (/^frontend/.test(file))
        frontendUpdated = true
    })
  })
  const args = []
  if (frontendUpdated)
    args.push('yarn')
  run_cmd('sh', ['./git_auto_deploy.sh', ...args], text => console.log(text))
})
