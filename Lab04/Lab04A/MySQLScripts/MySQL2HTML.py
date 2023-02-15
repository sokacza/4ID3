#
#   Simple SQL Database Parser
#   Adam Sokacz
#   2023 - 02 - 15
#

#   Libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import json
import mysql.connector
from mysql.connector import Error

HOST_IP = "localhost"
USER = "root"
PASSWORD = "9055259140"
DB_NAME = "iot"
TABLE_NAME = "data"

#   HTTP Server
HTTP_IP = '0.0.0.0'
HTTP_PORT = 3000


#   Handles when a device makes a POST or GET request to HTTP server
class requestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        global uiDict
        if self.path.endswith('/ui'):
            self.send_response(200)
            self.end_headers()
            connection = mysql.connector.connect(host=HOST_IP,
                                            user=USER,
                                            password=PASSWORD,
                                            database=DB_NAME)
            try:
                cursor = connection.cursor()  
                cursor.execute(f"""SELECT * FROM `{DB_NAME}`.`{TABLE_NAME}` WHERE `{TABLE_NAME}`.`iddata` < 40 ORDER BY `{TABLE_NAME}`.`iddata` DESC; """)
                table = cursor.fetchall()
                out = """
                    <style rel="stylesheet" type="text/css" media="screen">
                    html {
                        background-color: #DCDCDC;
                        margin: 0px 0px;
                        padding: 0px 0px;
                    }
                    ul { 
                        list-style-type: none; 
                    }
                    li {
                        font-size: 18pt;
                    }
                    fieldset {
                        background-color: white;
                        border: solid 3px #9c9c9c;
                        width: 400px;
                    }
                    legend {
                        font-size: 20pt;
                        font-weight: bold;
                    }
                    </style>"""

                for row in table:
                    out += f"""
                        <fieldset>
                            <legend>{row[1]}</legend>
                            <ul>
                                <li><i>Field: </i>{row[2]}</li>
                                <li><i>Value: </i>{row[3]}</li>
                            </ul>
                        </fieldset><br />"""

    
                cursor.close() 
                connection.commit()
                connection.close()


                
            except Error as e:
                print(f"DB Query Error", e)

            self.wfile.write(f"""
                    <html>
                    <body style="padding-left: 100px;">
                    <br />
                        <h1>DATABASE PARSER</h1>
                        <br/>
                        {out}
                    </body>
                    </html>
                    """.encode())
            


def main():
    #Tuple that stores the HTTP server data
    serverAddress = (HTTP_IP, HTTP_PORT)
    #Instantiate the server object
    server = HTTPServer(serverAddress, requestHandler)
    #Print useful data to the terminal
    print('\n\n---------------------\
        \nSimple HTTP IoT Server\n---\
        ------------------\n\n')
    print(f'HTTP server running on {HTTP_IP} port {HTTP_PORT}')
    print("\n\nServer Ready\n")
    #Serve the page until the thread exits
    server.serve_forever()

if __name__ == '__main__':
    main()




