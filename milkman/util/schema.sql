-- Table for storing warnings given to users by moderators.
CREATE TABLE IF NOT EXISTS `warns` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` TEXT NOT NULL,
    `guild_id` TEXT NOT NULL,
    `moderator_id` TEXT NOT NULL,
    `reason` TEXT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);