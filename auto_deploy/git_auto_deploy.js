const http = require('http');
const createHandler = require('github-webhook-handler');
const spawn = require('child_process').spawn;

function run_cmd(cmd, args, callback) {
  const child = spawn(cmd, args);
  let resp = '';
  let finished = 0;

  child.stderr.on('data', buffer => resp += buffer.toString());
  child.stdout.on('data', buffer => resp += buffer.toString());
  child.stderr.on('end', () => {
    if (++finished === 2) {
      callback(resp);
    }
  });
  child.stdout.on('end', () => {
    if (++finished === 2) {
      callback(resp);
    }
  });
}

const handler = createHandler({
    path: '/github-push',
    secret: 'shroud'
});

http.createServer((req, res) => {
  handler(req, res, err => {
    res.statusCode = 404;
    res.end('no such location');
  })
}).listen(8765);

handler.on('error', err => {
  console.error('Error:', err.message);
});

handler.on('push', event => {
  console.log('Received a push event for %s to %s',
    event.payload.repository.name,
    event.payload.ref);
  if (event.payload.ref !== 'refs/heads/site')
    return;

  let frontendUpdated = false;
  let frontendDependencyUpdated = false;
  let backendDependencyUpdated = false;
  let backendModelsUpdated = false;
  event.payload.commits.forEach(commit => {
    ['added', 'removed', 'modified'].forEach(ele => {
      commit[ele].forEach(file => {
        if (file.match('frontend'))
          frontendUpdated = true;
        if (file.match('frontend/package.json') || file.match('frontend/yarn.lock'))
          frontendDependencyUpdated = true;
        if (file.match('backend/models.py'))
          backendModelsUpdated = true;
        if (file.match('requirements.pip'))
          backendDependencyUpdated = true;
      });
    });
  });

  const args = [];
  if (frontendDependencyUpdated)
    args.push('-y');
  else if (frontendUpdated)
    args.push('-f');
  if (backendDependencyUpdated)
    args.push('-p');
  if (backendModelsUpdated)
    args.push('-b');
  run_cmd('sh', ['./git_auto_deploy.sh', ...args], text => console.log(text));
});
