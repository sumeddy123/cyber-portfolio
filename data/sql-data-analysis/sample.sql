-- Synthetic accounts and documentation-only IP addresses.
INSERT INTO users VALUES (1, 'alex'), (2, 'sam'), (3, 'riley');
INSERT INTO login_events VALUES
(1,1,'192.0.2.10','2026-01-01T10:00:00Z','failure'),
(2,1,'192.0.2.10','2026-01-01T10:01:00Z','failure'),
(3,1,'192.0.2.10','2026-01-01T10:02:00Z','failure'),
(4,1,'192.0.2.10','2026-01-01T10:03:00Z','success'),
(5,2,'198.51.100.20','2026-01-01T11:00:00Z','success'),
(6,2,'198.51.100.20','2026-01-01T11:01:00Z','failure');
