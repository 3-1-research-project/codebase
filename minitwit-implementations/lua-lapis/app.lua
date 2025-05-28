local lapis = require("lapis")
local User = require("models.user")

local app = lapis.Application()

app:enable("etlua")
app.layout = require "views.layout"

app:match("/static/*path", function(self)
    return self:send_file("static/" .. self.params.path)
end)

app:get("/", function()
  return { render = "timeline" }
end)

app:get("/register", function()
  return { render = "register" }
end)

app:post("/register", function (self)
  local username = self.params.username
  local email = self.params.email
  local password = self.params.password
  local user = {
    username = username,
    email = email,
    password = password
  }

  User:create(user)
  -- User.create_user(user)
end)

return app
