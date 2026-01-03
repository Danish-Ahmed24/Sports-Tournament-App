# Product Requirements Document (PRD)
## Football Transfer & Match Management System

**Version:** 1.0  
**Project Type:** CS50W Final Project  
**Timeline:** 2 Weeks (14 Days)  
**Developer:** Solo Project  
**Last Updated:** January 2026

---

## 1. Executive Summary

### 1.1 Product Vision
A web-based football management platform that enables players, team managers, and referees to interact in a realistic transfer market and match coordination system. The platform simulates real-world football operations including contract negotiations, democratic referee selection, and match result management.

### 1.2 Problem Statement
Traditional tournament management systems lack the business logic and role-based workflows found in professional sports. There's no educational platform that demonstrates:
- Transfer market mechanics with contract negotiations
- Democratic voting systems for match officials
- Multi-stakeholder workflows with different permissions
- State-based player availability management

### 1.3 Success Metrics
- All three user roles can complete their core workflows independently
- Transfer invitations successfully change player availability states
- Referee voting system correctly handles ties with experience-based tiebreaker
- Only authorized referees can submit match results
- System demonstrates complexity beyond basic CRUD operations

---

## 2. User Personas

### 2.1 Player (Primary User)
**Profile:**
- Name: Ahmed, 24 years old
- Position: Midfielder
- Goal: Get signed to a good team with fair salary

**Needs:**
- Browse teams looking for players
- Receive and compare multiple contract offers
- Accept offers when terms are favorable
- View upcoming matches and responsibilities

**Pain Points:**
- Receiving offers from teams that don't match skill level
- Not knowing which teams are actively recruiting
- Managing multiple simultaneous offers

---

### 2.2 Manager (Primary User)
**Profile:**
- Name: Sarah
- Role: Team Manager
- Goal: Build a competitive team and win matches

**Needs:**
- Browse available players (free agents)
- Send formal contract invitations with salary details
- Track invitation status (pending/accepted/rejected)
- Participate in referee selection for matches
- View team roster and upcoming fixtures

**Pain Points:**
- Players already signed showing in search results
- Not knowing if player received/saw invitation
- Missing voting deadlines for referee selection

---

### 2.3 Referee (Secondary User)
**Profile:**
- Name: Carlos
- Role: Match Official
- Goal: Officiate matches fairly and submit accurate results

**Needs:**
- Get selected for matches through fair voting
- Access match assignment details
- Submit match results with scores
- View officiating history and experience level

**Pain Points:**
- Bias in referee selection
- Disputes over who should officiate
- Manual result submission errors

---

## 3. Core Features & Requirements

### 3.1 User Authentication & Roles

**Priority:** P0 (Critical)  
**User Story:** "As a new user, I want to register and choose my role so I can access role-specific features."

#### Functional Requirements:
- **FR-3.1.1:** Users must register with email, password, and role selection (Player/Manager/Referee)
- **FR-3.1.2:** Role selection must be permanent after registration (cannot change roles)
- **FR-3.1.3:** Each role must have distinct profile fields:
  - Player: name, position, age, experience (years)
  - Manager: name, team name (created during registration)
  - Referee: name, experience (years, used for tiebreaker)
- **FR-3.1.4:** System must validate email uniqueness
- **FR-3.1.5:** Passwords must be hashed using Django's authentication system
- **FR-3.1.6:** Users must be able to log in and log out
- **FR-3.1.7:** Session must persist across page loads

#### Acceptance Criteria:
- ✅ Registration form shows role dropdown with 3 options
- ✅ Player registration requires position field
- ✅ Manager registration auto-creates a Team
- ✅ Referee registration requires experience field
- ✅ Login redirects to role-specific dashboard
- ✅ Logged-out users cannot access protected pages

---

### 3.2 Player Management & Profiles

**Priority:** P0 (Critical)  
**User Story:** "As a manager, I want to browse available players so I can find talent for my team."

#### Functional Requirements:
- **FR-3.2.1:** Players must have profiles with: name, position, age, experience, availability status
- **FR-3.2.2:** Availability status must be: "Available" (free agent) or "Signed" (on a team)
- **FR-3.2.3:** System must display "Browse Players" page listing all available players
- **FR-3.2.4:** Managers must NOT see players who are already signed
- **FR-3.2.5:** Players must NOT see players who are already signed (when availability == "Signed")
- **FR-3.2.6:** Player profile page must show: stats, current team (if signed), invitation history
- **FR-3.2.7:** System must update availability automatically when invitation accepted

#### Acceptance Criteria:
- ✅ Browse page shows only available players
- ✅ Player cards display position, age, experience
- ✅ Clicking player opens detailed profile
- ✅ Signed players have team badge/name visible
- ✅ Available players show "Send Invitation" button (for managers)

#### Business Rules:
- Player can only be on ONE team at a time
- Accepting invitation changes status to "Signed"
- Rejecting invitation keeps status as "Available"
- Players must manually leave team to become available again

---

### 3.3 Transfer Invitation System

**Priority:** P0 (Critical - Unique Feature!)  
**User Story:** "As a manager, I want to send contract offers to players so I can recruit them to my team."

#### Functional Requirements:
- **FR-3.3.1:** Managers must be able to send invitations to available players
- **FR-3.3.2:** Invitation must include:
  - Player name (auto-filled)
  - Team name (auto-filled from manager's team)
  - Salary offer (decimal, required)
  - Contract length in months (integer, required)
  - Personal message (text, optional)
- **FR-3.3.3:** Invitation must have status: Pending / Accepted / Rejected
- **FR-3.3.4:** New invitations default to "Pending"
- **FR-3.3.5:** Players must see list of all invitations sent to them
- **FR-3.3.6:** Players can accept OR reject invitations
- **FR-3.3.7:** When accepted:
  - Player joins manager's team
  - Player availability → "Signed"
  - All other pending invitations to this player auto-rejected
  - Invitation status → "Accepted"
- **FR-3.3.8:** When rejected:
  - Player remains available
  - Invitation status → "Rejected"
- **FR-3.3.9:** Managers cannot send duplicate invitations to same player
- **FR-3.3.10:** Managers must see status of all invitations they've sent

#### Acceptance Criteria:
- ✅ "Send Invitation" form validates salary > 0
- ✅ Player sees invitation with all details (team, salary, contract)
- ✅ Accept button immediately updates player's team
- ✅ Other pending invitations disappear after accepting one
- ✅ Manager sees "Accepted" badge on successful invitations
- ✅ Cannot send invitation to already-signed player

#### Business Rules:
- Manager can send multiple invitations simultaneously
- Player can have multiple pending invitations
- First accepted invitation wins (others auto-reject)
- Managers cannot retract sent invitations

---

### 3.4 Team Management

**Priority:** P1 (High)  
**User Story:** "As a manager, I want to view my team roster so I can see who I've recruited."

#### Functional Requirements:
- **FR-3.4.1:** Each manager must have exactly ONE team
- **FR-3.4.2:** Team must have: name, creation date, manager (one-to-one)
- **FR-3.4.3:** Team must display roster of all signed players
- **FR-3.4.4:** Team page must show:
  - Team name
  - Manager name
  - List of players with positions
  - Team statistics (optional: total players, avg experience)
- **FR-3.4.5:** Managers must be able to remove players from roster
- **FR-3.4.6:** Removing player sets their availability back to "Available"

#### Acceptance Criteria:
- ✅ My Team page shows all current players
- ✅ Each player card shows name, position, experience
- ✅ "Remove from Team" button changes player status
- ✅ Removed players reappear in "Browse Players"

---

### 3.5 Match System

**Priority:** P1 (High)  
**User Story:** "As a manager, I want to see upcoming matches so I know when my team plays."

#### Functional Requirements:
- **FR-3.5.1:** System must support match creation (by admin or manager)
- **FR-3.5.2:** Match must include:
  - Team A (foreign key to Team)
  - Team B (foreign key to Team)
  - Match date/time
  - Status: Scheduled / Voting / Completed
  - Assigned referee (foreign key to User, nullable)
- **FR-3.5.3:** Matches default to "Scheduled" status
- **FR-3.5.4:** System must display match list page with:
  - Upcoming matches (status = Scheduled or Voting)
  - Completed matches (status = Completed)
- **FR-3.5.5:** Match detail page must show:
  - Teams playing
  - Match date/time
  - Current status
  - Assigned referee (if voting completed)
  - Results (if completed)

#### Acceptance Criteria:
- ✅ Matches page separates upcoming/completed
- ✅ Match cards show team names and date
- ✅ Clicking match opens detail page
- ✅ Status badge color-coded (blue=scheduled, yellow=voting, green=completed)

---

### 3.6 Referee Voting System

**Priority:** P0 (Critical - Unique Feature!)  
**User Story:** "As a manager, I want to vote for referees so match officials are selected fairly."

#### Functional Requirements:
- **FR-3.6.1:** Each match must have a voting period before it occurs
- **FR-3.6.2:** During voting period, managers can vote for ONE referee per match
- **FR-3.6.3:** Managers can only vote for matches involving their team
- **FR-3.6.4:** Vote must record: match, manager, referee voted for, timestamp
- **FR-3.6.5:** Managers cannot change vote after submission
- **FR-3.6.6:** Voting period must have deadline (e.g., 24 hours before match)
- **FR-3.6.7:** After deadline, system must:
  - Count votes per referee
  - Assign referee with most votes
  - Handle ties: select referee with higher experience
  - Update match status to "Voting Complete"
  - Set assigned_referee field
- **FR-3.6.8:** Only assigned referee can submit match results
- **FR-3.6.9:** System must display voting status: "Voting Open" / "Voting Closed" / "Referee Assigned"

#### Acceptance Criteria:
- ✅ Voting page shows all available referees
- ✅ Each referee card shows name and experience
- ✅ Submit vote button confirms selection
- ✅ Cannot vote twice for same match
- ✅ After deadline, match shows assigned referee
- ✅ Tiebreaker correctly picks more experienced referee
- ✅ Non-participating managers cannot vote

#### Business Rules:
- Both team managers must vote (or system uses default logic)
- If no votes, assign random referee or most experienced
- Referee cannot vote for themselves
- Voting deadline enforced server-side (not just UI)

---

### 3.7 Match Result Submission

**Priority:** P1 (High)  
**User Story:** "As an assigned referee, I want to submit match results so they're recorded officially."

#### Functional Requirements:
- **FR-3.7.1:** Only assigned referee can submit results for a match
- **FR-3.7.2:** Result submission form must include:
  - Team A score (integer, required)
  - Team B score (integer, required)
  - Match notes (text, optional)
- **FR-3.7.3:** Scores must be non-negative integers
- **FR-3.7.4:** Submitting results must:
  - Create MatchResult record
  - Update match status to "Completed"
  - Record submission timestamp
- **FR-3.7.5:** Results cannot be edited after submission (or only by admin)
- **FR-3.7.6:** Match detail page must display results after completion
- **FR-3.7.7:** System must calculate winner based on scores

#### Acceptance Criteria:
- ✅ Only assigned referee sees "Submit Result" button
- ✅ Form validates scores >= 0
- ✅ Submission success message displayed
- ✅ Match status changes to "Completed"
- ✅ Results visible on match page: "Team A 3 - 1 Team B"
- ✅ Winner highlighted with badge/color

---

### 3.8 Dashboard Views (Role-Based)

**Priority:** P1 (High)  
**User Story:** "As a user, I want to see information relevant to my role when I log in."

#### Player Dashboard:
- **FR-3.8.1:** Must display:
  - Current team (if signed) or "Free Agent" status
  - Pending invitations with accept/reject buttons
  - Accepted/rejected invitation history
  - Upcoming matches (if on a team)

#### Manager Dashboard:
- **FR-3.8.2:** Must display:
  - My team roster with player count
  - Sent invitations with status
  - Upcoming matches requiring referee votes
  - Quick links: Browse Players, Send Invitation

#### Referee Dashboard:
- **FR-3.8.3:** Must display:
  - Matches assigned to referee
  - Pending result submissions
  - Match history (completed)
  - Total matches officiated

#### Acceptance Criteria:
- ✅ Login redirects to appropriate dashboard
- ✅ Dashboard shows only relevant data for user's role
- ✅ Quick action buttons for common tasks
- ✅ Count badges for pending actions (e.g., "3 pending invitations")

---

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-4.1.1:** Page load time under 3 seconds on standard connection
- **NFR-4.1.2:** Database queries optimized with select_related/prefetch_related
- **NFR-4.1.3:** System handles up to 100 users, 50 teams, 200 matches

### 4.2 Security
- **NFR-4.2.1:** All passwords hashed with PBKDF2
- **NFR-4.2.2:** CSRF protection enabled on all forms
- **NFR-4.2.3:** Permission checks on every view (login_required, role checks)
- **NFR-4.2.4:** SQL injection prevented via Django ORM
- **NFR-4.2.5:** XSS protection via template auto-escaping

### 4.3 Usability
- **NFR-4.3.1:** Interface responsive on mobile (320px+)
- **NFR-4.3.2:** Forms provide clear validation messages
- **NFR-4.3.3:** Success/error messages displayed after actions
- **NFR-4.3.4:** Navigation consistent across all pages
- **NFR-4.3.5:** No page should require more than 3 clicks from dashboard

### 4.4 Maintainability
- **NFR-4.4.1:** Code follows PEP 8 style guidelines
- **NFR-4.4.2:** Models have docstrings explaining purpose
- **NFR-4.4.3:** Business logic centralized in models/utils, not views
- **NFR-4.4.4:** Database schema documented

---

## 5. Database Schema

### Core Models:

```python
User (extends AbstractUser)
├── role: CharField (Player/Manager/Referee)
├── experience: IntegerField (years, for tiebreaker)
└── related: Player, Manager, Referee profiles

Player (OneToOne with User, if role=Player)
├── position: CharField (Forward/Midfielder/Defender/Goalkeeper)
├── age: IntegerField
├── availability: CharField (Available/Signed)
├── current_team: ForeignKey(Team, null=True)
└── stats: JSONField (optional, for future expansion)

Team
├── name: CharField (unique)
├── manager: OneToOneField(User)
├── created_at: DateTimeField
└── players: ManyToManyField(User, related_name='teams')

Invitation
├── manager: ForeignKey(User, related_name='sent_invitations')
├── player: ForeignKey(User, related_name='received_invitations')
├── team: ForeignKey(Team)
├── salary_offer: DecimalField(max_digits=10, decimal_places=2)
├── contract_length: IntegerField (months)
├── message: TextField (optional)
├── status: CharField (Pending/Accepted/Rejected)
├── created_at: DateTimeField
└── updated_at: DateTimeField

Match
├── team_a: ForeignKey(Team, related_name='home_matches')
├── team_b: ForeignKey(Team, related_name='away_matches')
├── match_date: DateTimeField
├── status: CharField (Scheduled/Voting/Completed)
├── assigned_referee: ForeignKey(User, null=True)
├── voting_deadline: DateTimeField
└── created_at: DateTimeField

RefereeVote
├── match: ForeignKey(Match)
├── manager: ForeignKey(User)
├── referee: ForeignKey(User)
├── voted_at: DateTimeField
└── unique_together: ['match', 'manager']

MatchResult
├── match: OneToOneField(Match)
├── score_a: IntegerField
├── score_b: IntegerField
├── notes: TextField (optional)
├── submitted_by: ForeignKey(User)
└── submitted_at: DateTimeField
```

---

## 6. User Workflows

### 6.1 Player Journey: Getting Signed

```
1. Register as Player → Enter name, position, age, experience
2. Login → See Player Dashboard
3. Status shows "Free Agent"
4. Wait for invitations OR browse teams
5. Receive invitation notification
6. View invitation details (team, salary, contract)
7. Accept invitation
   ↓
8. Status changes to "Signed"
9. Team name appears on profile
10. See upcoming matches on dashboard
```

### 6.2 Manager Journey: Building a Team

```
1. Register as Manager → Enter name, team name
2. Login → See Manager Dashboard
3. Team roster empty initially
4. Click "Browse Players"
5. Filter by position/experience
6. Select player → "Send Invitation"
7. Fill form: salary, contract length, message
8. Submit invitation
9. Wait for player response
10. Receive notification: "Accepted"
11. Player appears in team roster
12. Repeat for more players
```

### 6.3 Manager Journey: Voting for Referee

```
1. Login → See upcoming match on dashboard
2. Click "Vote for Referee" link
3. See list of all referees with experience
4. Select one referee
5. Confirm vote
6. See "Vote Submitted" message
7. Wait for voting deadline
8. After deadline → See assigned referee on match page
```

### 6.4 Referee Journey: Submitting Results

```
1. Login → See Referee Dashboard
2. View assigned matches
3. After match occurs → Click "Submit Result"
4. Enter Team A score, Team B score
5. Add optional notes
6. Submit form
7. Match status changes to "Completed"
8. Results visible publicly
```

---

## 7. Development Timeline (14 Days)

### Phase 1: Foundation (Days 1-4)
**Day 1:** ✅ Project setup, base templates (DONE)
**Day 2:** User authentication with roles, registration forms
**Day 3:** Player profiles, browse players page
**Day 4:** Team creation, team roster view

### Phase 2: Core Features (Days 5-9)
**Day 5:** Invitation model, send invitation form
**Day 6:** Player view invitations, accept/reject logic
**Day 7:** Match model, match list/detail pages
**Day 8:** Referee voting model, voting form
**Day 9:** Vote counting logic, assign referee with tiebreaker

### Phase 3: Completion (Days 10-13)
**Day 10:** Match result submission form
**Day 11:** Result display, winner calculation
**Day 12:** Dashboards for all three roles
**Day 13:** Permissions, testing, bug fixes

### Phase 4: Polish (Day 14)
**Day 14:** Documentation, README, demo video

---

## 8. Out of Scope (Future Enhancements)

### Post-CS50W Features:
- ❌ Real-time chat between players and managers
- ❌ Formation builder with drag-and-drop
- ❌ Excel file upload for match results
- ❌ Advanced statistics and analytics dashboard
- ❌ Player-to-player messaging
- ❌ Notification system (email/push)
- ❌ Payment processing for salaries
- ❌ Contract expiration tracking
- ❌ Transfer deadline day mechanics
- ❌ Player injury/suspension system
- ❌ Match highlights/commentary
- ❌ League tables and tournaments

---

## 9. Success Criteria & Distinctiveness

### CS50W Requirements Met:

✅ **Distinctiveness:**
- Transfer invitation system with state management (not in course)
- Democratic voting mechanism with tiebreaker logic (unique)
- Three distinct role-based workflows (complex permissions)
- Multi-step business processes (invitation flow, voting flow)

✅ **Complexity:**
- 7+ models with complex relationships
- State-based logic (player availability, match status)
- Calculated fields (vote counting, winner determination)
- Role-based access control throughout

✅ **Mobile Responsive:**
- Bootstrap 5 grid system
- Responsive navigation
- Touch-friendly controls

✅ **JavaScript (Will Add in Week 2):**
- AJAX invitation accept/reject (no page reload)
- Dynamic vote submission
- Real-time vote count updates
- Client-side form validation

✅ **Files:**
- Separate Python files for models, views, forms, utils
- Multiple templates with inheritance
- Static files (CSS, JS)
- Clear project structure

---

## 10. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Voting logic complexity | Medium | High | Start early, write tests, use simple counting |
| Time running out | High | High | Prioritize P0 features, skip nice-to-haves |
| State management bugs | Medium | Medium | Test invitation flow thoroughly |
| Permission edge cases | Medium | Medium | Checklist of all permission scenarios |
| JavaScript debugging | Low | Low | Use simple vanilla JS, test incrementally |

---

## 11. Testing Checklist

### Manual Test Cases:

**Player Tests:**
- [ ] Register as player with all positions
- [ ] Receive invitation from manager
- [ ] Accept invitation → status becomes "Signed"
- [ ] Accept invitation → other invitations auto-reject
- [ ] Reject invitation → status remains "Available"
- [ ] Cannot accept invitation if already signed

**Manager Tests:**
- [ ] Register as manager → team auto-created
- [ ] Browse only available players
- [ ] Send invitation with valid salary
- [ ] Cannot send duplicate invitation to same player
- [ ] View sent invitation status
- [ ] Vote for referee before deadline
- [ ] Cannot vote twice for same match

**Referee Tests:**
- [ ] Register as referee with experience
- [ ] View assigned matches
- [ ] Submit result with valid scores
- [ ] Cannot submit result for unassigned match
- [ ] Results visible after submission

**System Tests:**
- [ ] Vote tie correctly uses experience tiebreaker
- [ ] Referee with more experience wins tie
- [ ] Match status progression: Scheduled → Voting → Completed
- [ ] Only logged-in users access protected pages
- [ ] Correct dashboard shown per role

---

## 12. Documentation Requirements

### README.md Must Include:
1. Project description and goals
2. Distinctiveness and complexity explanation
3. File structure and what each file does
4. How to run the project
5. User roles and their capabilities
6. Unique features (invitations, voting)
7. Technologies used
8. Future enhancements

### Code Documentation:
- Docstrings for all models explaining purpose
- Comments for complex logic (voting, state changes)
- Inline comments for non-obvious code

### Demo Video:
- Under 2 minutes for CS50W
- Show all three user roles
- Demonstrate invitation workflow
- Show voting system in action
- Display match result submission

---

## Appendix A: Key Terms

- **Free Agent:** Player not currently on any team (availability = "Available")
- **Signed Player:** Player currently on a team (availability = "Signed")
- **Invitation:** Formal contract offer from manager to player
- **Voting Period:** Time window when managers vote for match referee
- **Tiebreaker:** Logic to select referee when vote counts are equal
- **Assigned Referee:** Referee selected through voting to officiate match
- **Match Status:** Current state of match (Scheduled/Voting/Completed)

---

**Document Approval:**

| Role | Name | Status |
|------|------|--------|
| Product Owner | [Your Name] | Draft Complete |
| Developer | [Your Name] | Ready to Implement |
| CS50W Staff | Pending | Awaiting Review |

---

*End of Product Requirements Document*