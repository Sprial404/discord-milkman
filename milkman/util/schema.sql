-- Table for storing warnings given to users by moderators.
CREATE TABLE IF NOT EXISTS `warns` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `user_id` TEXT NOT NULL,
    `guild_id` TEXT NOT NULL,
    `moderator_id` TEXT NOT NULL,
    `reason` TEXT NOT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for persisting the temporary channels created by the bot.
CREATE TABLE IF NOT EXISTS `temporary_channels` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `channel_id` TEXT NOT NULL,
    `guild_id` TEXT NOT NULL,
    `creator_id` TEXT NOT NULL,
    `is_deleted` BOOLEAN NOT NULL DEFAULT 0,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `deleted_at` DATETIME DEFAULT NULL,
    UNIQUE (`channel_id`, `guild_id`)
);

CREATE INDEX IF NOT EXISTS `idx_temporary_channels_is_deleted` ON `temporary_channels` (`is_deleted`);