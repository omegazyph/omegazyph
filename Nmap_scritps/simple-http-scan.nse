-- HEAD
local stdnse = require "stdnse"
local shortport = require "shortport"

description = [[
  simple http scan  A script to see if http-alt is open and print information about it.
]]

author = "Wayne Stock"

license = "Same as Nmap--See https://nmap.org/book/man-legal.html"
 
categories = {"safe"}



-- RULES
portrule = shortport.port_or_service(8000,"http-alt")



-- ACTION
action = function(host, port)
        return port.version.name .. " is " .. port.state .. " and running on port number " .. port.number .. "."
end
