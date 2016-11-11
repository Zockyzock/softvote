DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
  voter_id INTEGER NOT NULL UNIQUE,
  vote VARCHAR(128) NOT NULL,
  vote_id VARCHAR(128) NOT NULL,
  PRIMARY KEY (voter_id, vote_id)
);
