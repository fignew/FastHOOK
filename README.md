# FastHOOK
## Github pokes, we touch
FastHOOK is a simple API for running actions via the Saltstack reactor system from webhooks.

This has the advantage of being able to run actions on systems that are not directly accessible from the internet.

## How it works

* Github pokes an endpoint hosted by FastHOOK
  * This system must be accessible from github (but the system being affected does not need to be)
  * This endpoint is in the form of `https://fasthook.example.edu/github/TARGET/HOOK`
  * Target is the minion id that we are wanting to run the action on
  * Hook is the name of the reactor that will be run on the target
* FastHOOK takes this input and touches the corresponding file in /run/fasthook
* The configured Salt beacon gets inotified that the file's attributes have changed (mtime)
* Saltstack reactor system picks up that the file has been updated and sends an event to the eventbus
* Salt reactor is called on targethost and ends up running webhook formula (in salt/webhook)
* Webhook formula looks up webhookname in hooklist.yml to determine which formula to run
