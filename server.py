from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SimpleAPI(BaseHTTPRequestHandler):
      
      
      users = ["Alice", "Bob"]

      def send_json(self, data, status=200):
        """
        send a JSON response to the client.

        Args:
        data(dict): python dictionary to be converted to JSON and sent as response
        status(int): HTTP status code for the response (default: 200)
        """

        # write http status code line (e.g HTTP/1.1 200 OK)
        self.send_response(status)

        #inform the client that the response is in JSON format
        self.send_header("Content-Type", "application/json")

        # Signal end of the http headers
        self.end_headers()

        # convert python dict -> JSON -> bytes and write to response stream
        self.wfile.write(json.dumps(data).encode())

      def do_GET(self):
        """
        Handle HTTP GET requests.
        Endpoint: /users - returns list of users
        """
        # route matching: check request url path
        if self.path == "/users":

            # send list of user with 200 OK status
            self.send_json({"users": self.users})
    
      def do_POST(self):
        """
        Handle HTTP POST requests:
        Endpoint: /users - creates a new user
        """
        if self.path == "/users":

            # Read content-length header to know body size
            content_length = int(self.headers.get("Content-Length", 0))

            # Read raw request body from socket(bytes)
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, status=400)
                return
            
            if "name" not in data:
                # Return 400 if 'name' is missing
                self.send_json({"error": "Name is required"}, 400)
                return
            
            # Add new user to the list and return updated list with 201 Created status
            self.users.append(data["name"])
            self.send_json(
                {"message": "User created", "users": self.users}, 201
            )  
# Create and start the server instance
server = HTTPServer(('localhost', 8000), SimpleAPI)

#Inform user that server has started
print("Server running at http://localhost:8000")

# Start the server to handle requests indefinitely until interrupted
server.serve_forever()                



