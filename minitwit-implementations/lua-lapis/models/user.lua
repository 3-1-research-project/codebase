local Model = require("lapis.db.model").Model

local User = Model:extend("users", {
    primary_key = "user_id",

    validations = {
        { "username", exists = true, min_length = 3, max_length = 32 },
        { "email", exists = true, min_length = 5, max_length = 255 },
        { "pw_hash", exists = true }
    }
})

function User:find_by_username(username)
    return User:find({ username = username })
end

function User:find_by_email(email)
    return User:find({ email = email })
end

function User:create_user(user)
    return User:create({user})
end

function User:get_followers()
    local db = require("lapis.db")
    local users = require("models.user")
    return users:select([[
        inner join followers on users.user_id = followers.who_id
        where followers.whom_id = ?
    ]], self.user_id)
end

function User:get_following()
    local db = require("lapis.db")
    local users = require("models.user")
    return users:select([[
        inner join followers on users.user_id = followers.whom_id
        where followers.who_id = ?
    ]], self.user_id)
end

return User