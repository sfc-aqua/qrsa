# controller

the controller manages, monitor, and debug qnodes.
there're two parts, one is the api server and the other is client.
the api server can access to qnodes to collect information.

# how to run

first of all, you need to start the api server.
```sh
$ python src/controller/main.py
```


and then you need to start the client in another terminal.

```sh
$ cd controller/client
$ npm install
$ npm run dev
```

then you can access to http://localhost:5173

