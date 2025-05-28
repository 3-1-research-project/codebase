local config = require("lapis.config")

local function parse_postgres_url(url)
  if not url or url == "" then
    error("DATABASE_URL is not set or empty")
  end
  -- protocol://user:password@host:port/database
  local user, password, host, port, database = url:match(
    "^postgresql://([^:]+):([^@]+)@([^:]+):(%d+)/(.+)$"
  )
  if not (user and password and host and port and database) then
    error("DATABASE_URL is malformed: " .. tostring(url))
  end
  return {
    user = user,
    password = password,
    host = host,
    port = port,
    database = database
  }
end


local database_url = os.getenv("DATABASE_URL")
print("database_url: " .. tostring(database_url))
local db_info = parse_postgres_url(database_url)

config("development", {
  server = "nginx",
  code_cache = "off",
  num_workers = "1",
  port = 5000,
  postgres = {
    host = db_info.host,
    user = db_info.user,
    password = db_info.password,
    database = db_info.database,
    port = db_info.port,
  }
})
