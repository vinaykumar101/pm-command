-- PM Command Center Database Schema
-- SQLite Migration: Populate Dummy Data

-- Insert Clients
INSERT INTO clients (name, industry, contact, email, phone, type, priority, engagement, contract, start_date, notes) VALUES
('DeHaat', 'AgriTech', 'Nikhil', 'nikhil@example.com', '9999999999', 'Enterprise', 'High', 'SaaS', 'Active', '2026-04-01', 'Field app and analytics dashboards'),
('Govt. Program', 'Public Sector', 'Program Officer', 'officer@example.gov', '8888888888', 'Government', 'High', 'Dashboard', 'Signed', '2026-04-08', 'Cluster and farmer lifecycle reporting'),
('FreshFoods', 'FMCG', 'Operations Head', 'ops@freshfoods.com', '7777777777', 'Partner', 'Medium', 'Integration', 'In Discussion', '2026-04-15', 'Procurement workflow and traceability');

-- Insert Projects (client_id = 1 for DeHaat, 2 for Govt. Program, 3 for FreshFoods)
INSERT INTO projects (name, client_id, type, problem, objective, users, metrics, owner, tech_owner, qa_owner, start_date, release_date, status, priority, risk) VALUES
('AgriPulse 2.0', 1, 'Mobile App', 'Field workflows are fragmented', 'Create offline-first field execution app', 'FSP, TOM, Admin', 'Onboarding %, attendance compliance', 'Saksham', 'Kshitij', 'Sampada', '2026-04-01', '2026-05-15', 'Development', 'High', 'Medium'),
('DigiAcre 2.0', 1, 'Dashboard', 'Reports lack role-based visibility', 'Create RBAC reporting hub', 'Admin, TOM, IVR Manager', 'Report usage, access accuracy', 'Saksham', 'Tech Team', 'QA Team', '2026-04-05', '2026-05-30', 'Design', 'High', 'High'),
('Cluster Monitoring', 2, 'Data Product', 'Manual progress tracking', 'Automated farmer and activity reporting', 'PMU, Govt Officers', 'Data completeness, dashboard refresh', 'Product Team', 'BI Team', 'Data QA', '2026-04-10', '2026-06-01', 'Requirement Gathering', 'Medium', 'Medium'),
('Traceability API', 3, 'API', 'Buyer needs farm-to-procurement traceability', 'Expose traceability data through API', 'Buyer Ops, Internal Ops', 'API uptime, matched lots', 'Platform PM', 'Backend Team', 'QA Team', '2026-04-20', '2026-06-15', 'Discovery', 'Medium', 'Low');

-- Insert Requirements
INSERT INTO requirements (title, client_id, project_id, type, source, description, need, problem, outcome, priority, status, requested_by, request_date) VALUES
('Mandatory attendance before task', 1, 1, 'Feature', 'UAT', 'FSP must check-in before any task', 'Improve field discipline', 'Tasks are done without attendance', 'Attendance-linked task execution', 'P0', 'Approved', 'Operations', '2026-04-17'),
('Transfer farmers between FSPs', 1, 2, 'Feature', 'Internal Team', 'Admin can transfer farmers from one FSP to another', 'Correct mapping', 'Manual reassignment is slow', 'Clean farmer-agent mapping', 'P1', 'Under Review', 'Ops Team', '2026-04-20'),
('Data validation tracker', 2, 3, 'Data Requirement', 'Leadership', 'Track report mismatches', 'Improve data trust', 'Manual validation gaps', 'Resolved data issues', 'P1', 'New', 'PMO', '2026-04-21');

-- Insert PRDs
INSERT INTO prds (title, client_id, project_id, background, problem, objective, users, personas, current_process, solution, journey, functional_req, nonfunctional_req, rbac, api_req, data_req, edge_cases, acceptance_criteria, dependencies, risks, metrics, outscope, release_plan, uat_plan, questions, status) VALUES
('AgriPulse Attendance Control', 1, 1, 'Attendance flow required for task discipline', 'Users can perform work without check-in', 'Block task activity without attendance', 'FSP, TOM', 'Field agent, manager', 'Open task access', 'Attendance gate before task flow', 'Login > Check-in > Task', 'Check-in validation before task', 'Fast and offline-aware', 'FSP enforced, Admin override', 'Attendance status API', 'Check-in timestamp and task logs', 'Offline, device time mismatch', 'Task blocked if not checked-in', 'Attendance API', 'Offline sync conflict', 'Attendance compliance', 'Payroll logic', 'Sprint 1', 'Field UAT', 'Device time validation', 'Approved');

-- Insert Tasks
INSERT INTO tasks (title, client_id, project_id, prd_id, type, description, acceptance_criteria, assigned_to, priority, status, sprint, due_date, estimate, actual_effort) VALUES
('Create attendance gate API', 1, 1, 1, 'API', 'Return active attendance status', 'API returns checked-in true/false', 'Backend Team', 'P0', 'In Progress', 'Sprint 1', '2026-05-02', '2d', '1d'),
('Update Home UI', 1, 1, 1, 'UI', 'Align home with Figma', 'UI matches approved design', 'Frontend Team', 'P1', 'QA', 'Sprint 1', '2026-05-05', '3d', '3d'),
('Create farmer transfer flow', 1, 2, NULL, 'Feature', 'Admin selects old FSP, new FSP and farmers', 'Selected farmers move to new FSP', 'Fullstack Team', 'P1', 'Backlog', 'Sprint 2', '2026-05-12', '4d', '-'),
('Validate cohort data', 2, 3, NULL, 'Data', 'Check retention values', 'No null cohort rows', 'Data QA', 'P2', 'To Do', 'Sprint 2', '2026-05-10', '1d', '-');

-- Insert Bugs
INSERT INTO bugs (title, description, steps_to_reproduce, expected_result, actual_result, severity, priority, assigned_to, status, environment, reported_by, reported_date, project_id) VALUES
('Image upload fails on weak network', 'Check-in image upload fails', 'Go offline/weak network > upload image', 'Image retries', 'Upload failed', 'High', 'P1', 'Mobile Team', 'Open', 'UAT', 'QA', '2026-04-18', 1),
('Wrong age calculation', 'DOB-based age mismatch', 'Open agent profile', 'Correct age', 'Age blank', 'Medium', 'P2', 'Frontend Team', 'In Progress', 'Dev', 'Saksham', '2026-04-19', 1);

-- Insert UAT Cases
INSERT INTO uat_cases (name, module, feature, expected_result, actual_result, status, severity, tester, test_date, remarks, task_id, prd_link) VALUES
('Login OTP', 'Auth', 'OTP auto-fetch', 'OTP auto-detected', 'Works', 'Pass', 'Low', 'Sampada', '2026-04-17', 'OK', NULL, 'Auth'),
('Offline onboarding', 'Farmer', 'Quick onboarding', 'Draft saved offline', 'Saved', 'Pass', 'Medium', 'QA', '2026-04-17', 'Needs sync validation', NULL, 'Farmer Onboarding'),
('Check-in image', 'Attendance', 'Image upload', 'Upload success', 'Failed on weak network', 'Fail', 'High', 'QA', '2026-04-17', 'Bug raised', NULL, 'Attendance');

-- Insert Validation Issues
INSERT INTO validation_issues (title, client_id, project_id, source, table_name, description, expected_data, actual_data, severity, owner, status, identified_date, notes) VALUES
('Dashboard count mismatch', 1, 2, 'Metabase', 'farmer_program', 'Active farmer count mismatch', '10,000', '9,742', 'High', 'Data Team', 'Open', '2026-04-22', 'Check duplicate filters'),
('Missing district filter values', 2, 3, 'Tableau', 'district dimension', 'Empty districts showing', 'Only districts with data', 'All districts', 'Medium', 'BI Team', 'In Progress', '2026-04-23', 'Filter data source');

-- Insert Releases
INSERT INTO releases (name, version, client_id, project_id, release_date, release_type, features, bugs_fixed, known_issues, deployment_status, uat_status, approval_status, notes) VALUES
('AgriPulse UAT Build', 'v0.9.1', 1, 1, '2026-04-17', 'Minor', 'Attendance, onboarding, KPI', 'Login fixes', 'Image upload weak network', 'Deployed', 'Pending', 'Pending', 'Shared for selected user acceptance'),
('DigiAcre RBAC Alpha', 'v0.5.0', 1, 2, '2026-05-05', 'Major', 'Role-based dashboards', '-', 'Report latency', 'Planned', 'Pending', 'Pending', 'Internal testing planned');

-- Insert Meetings
INSERT INTO meetings (title, client_id, project_id, meeting_date, attendees, discussion_points, decisions, action_items, owner, due_date, status) VALUES
('UAT Readiness Review', 1, 1, '2026-04-17', 'Product, Tech, QA', 'Module readiness and defects', 'Share build with selected users', 'Close P0 bugs', 'Product', '2026-04-22', 'Closed');

-- Insert Metrics
INSERT INTO metrics (name, current_value, target_value, status, trend) VALUES
('DAU', '1,240', '1,500', 'Amber', 'Up'),
('WAU', '5,980', '6,500', 'Amber', 'Up'),
('MAU', '18,400', '20,000', 'Amber', 'Stable'),
('Activation Rate', '62%', '70%', 'Amber', 'Up'),
('Retention Rate', '54%', '60%', 'Amber', 'Stable'),
('Churn Rate', '8%', '5%', 'Red', 'Down'),
('Feature Adoption', '71%', '75%', 'Green', 'Up'),
('Task Completion', '84%', '90%', 'Amber', 'Up'),
('Error Rate', '3.2%', '1%', 'Red', 'Down'),
('UAT Pass %', '67%', '90%', 'Red', 'Stable');

-- Insert Funnel Stages
INSERT INTO funnel_stages (stage_name, user_count, display_order) VALUES
('User Registered', 10000, 1),
('Profile Completed', 8200, 2),
('First Action Performed', 6100, 3),
('Feature Used', 4700, 4),
('Task Completed', 3900, 5),
('Activated', 2800, 6);

-- Insert Cohorts
INSERT INTO cohorts (cohort_date, day0, day1, day7, day14, day30, day60, day90) VALUES
('2026-04-01', '100%', '78%', '61%', '52%', '44%', '36%', '29%'),
('2026-04-08', '100%', '82%', '64%', '55%', '46%', '38%', '-'),
('2026-04-15', '100%', '75%', '58%', '49%', '-', '-', '-'),
('2026-04-22', '100%', '69%', '-', '-', '-', '-', '-');

-- Insert Reports
INSERT INTO reports (name, description, last_updated) VALUES
('Client-wise Project Status Report', 'Shows project progress by client', '2026-04-25'),
('PRD Progress Report', 'Tracks PRDs by status', '2026-04-24'),
('Task Completion Report', 'Sprint and owner-wise task completion', '2026-04-24'),
('Funnel Drop-off Report', 'Stage-wise funnel drop-off', '2026-04-23'),
('Cohort Retention Report', 'Retention cohort performance', '2026-04-23'),
('Data Validation Report', 'Open and resolved data issues', '2026-04-22'),
('Release Readiness Report', 'UAT, bugs and deployment readiness', '2026-04-21');