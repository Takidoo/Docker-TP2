var DbName = process.env.MONGO_INITDB_DATABASE || "blog_db";
var appUsername = process.env.MONGO_APP_USERNAME || "blog_admin";
var appPassword = process.env.MONGO_APP_PASSWORD || "blog_password";
var Db = db.getSiblingDB(DbName);

if (!Db.getUser(appUsername)) {
    targetDb.createUser({
        user: appUsername,
        pwd: appPassword,
        roles: [{ role: "readWrite", db: DbName }]
    });
}

if (!Db.getCollectionNames().includes("posts")) {
    Db.createCollection("posts", {
        validator: {
            $jsonSchema: {
                title: "Post Schema",
                required: ["title", "content", "author"],
                properties: {
                    title: {
                        type: "string",
                        maxLength: 100
                    },
                    content: {
                        type: "string",
                        maxLength: 2000
                    },
                    author: {
                        type: "string",
                        maxLength: 30
                    }
                }
            }
        },
        validationAction: "error",
        validationLevel: "strict"
    });
}

if (Db.posts.countDocuments() === 0) {
    Db.posts.insertMany([
        {
            title: "Post 1",
            content: "Content 1",
            author: appUsername
        },
        {
            title: "Post 2",
            content: "Content 2",
            author: appUsername
        },
        {
            title: "Post 3",
            content: "Content 3",
            author: appUsername
        },
        {
            title: "Post 4",
            content: "Content 4",
            author: appUsername
        },
        {
            title: "Post 5",
            content: "Content 5",
            author: appUsername
        }
    ]);
}