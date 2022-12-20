
// In your web server, before serving the plugin HTML, get the auth_secret from the plugin's URL and verify that it matches the one saved.
// const frontPluginSecret = req.query.auth_secret;


// If the auth_secret does not match, the plugin does not come from Front.
// if (frontPluginSecret !== '8fe18727dcad37f9')
//   return res.sendStatus(401);

// ...proceed with the request.