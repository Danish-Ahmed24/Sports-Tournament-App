# 🏆 Sports Tournament App - Development Tracker

**Project:** CS50W Final Project  
**Timeline:** 2 Weeks  
**Status:** Not Started

---

## 📋 Quick Reference - What Am I Building?

A sports tournament management system where:
- Users have roles (Player, Captain, Referee, Admin)
- Captains create teams, players join them
- Admins create tournaments and matches
- Referees submit match results and player stats
- System **calculates** winners, MVPs, and leaderboards automatically
- Heavy JavaScript for dynamic updates (no page reloads)

---

## ✅ Development Checklist

### 🔧 Phase 1: Project Setup (Day 1)
- [ ] Create Django project: `django-admin startproject sports_tournament`
- [ ] Create app: `python manage.py startapp tournament`
- [ ] Add app to `INSTALLED_APPS` in settings.py
- [ ] Set up static files and templates folders
- [ ] Install Bootstrap 5 (CDN in base.html)
- [ ] Create `base.html` template with navbar
- [ ] Run initial migration: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Test server runs: `python manage.py runserver`

**Git Commit:** "Initial project setup"

---

### 👤 Phase 2: User System (Day 2)

#### Models to Create (models.py)
- [ ] Extend User model with `role` field (Player/Captain/Referee/Admin)
  ```python
  from django.contrib.auth.models import AbstractUser
  
  class User(AbstractUser):
      ROLES = [('player', 'Player'), ('captain', 'Captain'), 
               ('referee', 'Referee'), ('admin', 'Admin')]
      role = models.CharField(max_length=10, choices=ROLES)
  ```
- [ ] Update `AUTH_USER_MODEL` in settings.py
- [ ] Make migrations: `python manage.py makemigrations`
- [ ] Migrate: `python manage.py migrate`

#### Views to Create (views.py)
- [ ] `register_view` - register new users with role selection
- [ ] `login_view` - log in users
- [ ] `logout_view` - log out users
- [ ] `profile_view` - show current user info

#### Templates to Create
- [ ] `register.html` - registration form with role dropdown
- [ ] `login.html` - login form
- [ ] `profile.html` - user profile page

#### URLs to Add (urls.py)
- [ ] `/register/`
- [ ] `/login/`
- [ ] `/logout/`
- [ ] `/profile/`

**Test:** Register as each role, log in, log out  
**Git Commit:** "Add user authentication and roles"

---

### ⚽ Phase 3: Sports & Teams (Day 3-4)

#### Models to Create
- [ ] **Sport** model
  ```python
  class Sport(models.Model):
      name = models.CharField(max_length=50, unique=True)
      allows_draws = models.BooleanField(default=True)
      points_for_win = models.IntegerField(default=3)
      points_for_draw = models.IntegerField(default=1)
  ```
- [ ] **Team** model
  ```python
  class Team(models.Model):
      name = models.CharField(max_length=100)
      sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
      captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captained_teams')
      players = models.ManyToManyField(User, related_name='teams', blank=True)
  ```
- [ ] **JoinRequest** model (optional, for approval system)
  ```python
  class JoinRequest(models.Model):
      player = models.ForeignKey(User, on_delete=models.CASCADE)
      team = models.ForeignKey(Team, on_delete=models.CASCADE)
      status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
      created_at = models.DateTimeField(auto_now_add=True)
  ```

- [ ] Make and run migrations

#### Views to Create
- [ ] `sports_list` - show all sports (anyone can view)
- [ ] `create_team` - captains can create teams
- [ ] `team_detail` - show team info and roster
- [ ] `join_team` - players request to join
- [ ] `manage_requests` - captains approve/reject requests
- [ ] `leave_team` - players leave teams

#### Templates to Create
- [ ] `sports_list.html`
- [ ] `create_team.html`
- [ ] `team_detail.html`
- [ ] `my_teams.html`

#### Permission Checks to Add
- [ ] Only captains can create teams
- [ ] Only team captain can approve join requests
- [ ] Only players on team can leave

**Test:** Create sport in admin, create team as captain, join as player  
**Git Commit:** "Add sports and team management"

---

### 🏆 Phase 4: Tournaments (Day 5)

#### Models to Create
- [ ] **Tournament** model
  ```python
  class Tournament(models.Model):
      name = models.CharField(max_length=100)
      sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
      format = models.CharField(max_length=20, choices=[('group', 'Group Stage'), ('knockout', 'Knockout')])
      teams = models.ManyToManyField(Team, related_name='tournaments')
      created_at = models.DateTimeField(auto_now_add=True)
  ```

- [ ] Make and run migrations

#### Views to Create
- [ ] `tournament_list` - show all tournaments
- [ ] `create_tournament` - admins create tournaments
- [ ] `tournament_detail` - show tournament info and teams
- [ ] `add_team_to_tournament` - admins add teams

#### Templates to Create
- [ ] `tournament_list.html`
- [ ] `create_tournament.html`
- [ ] `tournament_detail.html`

#### Permission Checks
- [ ] Only admins can create tournaments
- [ ] Only teams from same sport can join tournament

**Test:** Create tournament as admin, add teams to it  
**Git Commit:** "Add tournament management"

---

### ⚽ Phase 5: Matches (Day 6-7)

#### Models to Create
- [ ] **Match** model
  ```python
  class Match(models.Model):
      tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
      team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_a')
      team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_team_b')
      referee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='refereed_matches')
      score_a = models.IntegerField(null=True, blank=True)
      score_b = models.IntegerField(null=True, blank=True)
      status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('locked', 'Locked')], default='scheduled')
      match_date = models.DateTimeField()
      
      def get_winner(self):
          # Calculate winner dynamically
          if self.score_a is None or self.score_b is None:
              return None
          if self.score_a > self.score_b:
              return self.team_a
          elif self.score_b > self.score_a:
              return self.team_b
          else:
              return "Draw" if self.tournament.sport.allows_draws else None
  ```

- [ ] Make and run migrations

#### Views to Create
- [ ] `create_match` - admins create matches
- [ ] `match_detail` - show match info
- [ ] `my_matches` - referees see their assigned matches
- [ ] `submit_result` - referees submit scores
- [ ] `lock_match` - referees lock completed matches

#### Templates to Create
- [ ] `create_match.html`
- [ ] `match_detail.html`
- [ ] `my_matches.html` (for referees)
- [ ] `submit_result.html`

#### Permission Checks
- [ ] Only admins can create matches
- [ ] Only assigned referee can submit/edit results
- [ ] Locked matches cannot be edited

**Test:** Create match, assign referee, submit result as referee  
**Git Commit:** "Add match management and result submission"

---

### 📊 Phase 6: Player Stats & MVP (Day 8-9)

#### Models to Create
- [ ] **StatWeight** model
  ```python
  class StatWeight(models.Model):
      sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
      stat_name = models.CharField(max_length=50)  # e.g., "goals", "assists"
      weight = models.IntegerField()  # e.g., 10 for goal, 5 for assist
      
      class Meta:
          unique_together = ['sport', 'stat_name']
  ```

- [ ] **PlayerMatchStats** model
  ```python
  class PlayerMatchStats(models.Model):
      player = models.ForeignKey(User, on_delete=models.CASCADE)
      match = models.ForeignKey(Match, on_delete=models.CASCADE)
      stat_name = models.CharField(max_length=50)
      stat_value = models.DecimalField(max_digits=5, decimal_places=2)
      
      def calculate_mvp_contribution(self):
          # Get weight for this stat
          weight = StatWeight.objects.get(sport=self.match.tournament.sport, stat_name=self.stat_name)
          return self.stat_value * weight.weight
  ```

- [ ] Make and run migrations
- [ ] Add stat weights in admin panel (e.g., Football: goals=10, assists=5, yellow_card=-2)

#### Views/Functions to Create
- [ ] `submit_player_stats` - referees add stats for players in match
- [ ] `calculate_match_mvp` - function to find MVP of a match
  ```python
  def calculate_match_mvp(match):
      # Get all stats for this match
      # Group by player
      # Sum (stat_value * weight) for each player
      # Return player with highest score
  ```
- [ ] `player_stats` - view to show all stats for a player
- [ ] `match_mvp_view` - show MVP for completed matches

#### Templates to Create
- [ ] `submit_stats.html` - form to add player stats
- [ ] `player_stats.html` - display player statistics
- [ ] Update `match_detail.html` to show MVP

**Test:** Add stats for players, verify MVP calculation  
**Git Commit:** "Add player statistics and MVP calculation"

---

### 📈 Phase 7: Leaderboards (Day 10)

#### Functions to Create (utils.py or in views)
- [ ] `calculate_tournament_standings(tournament)`
  ```python
  def calculate_tournament_standings(tournament):
      # For each team in tournament:
      #   - Count matches played
      #   - Count wins/draws/losses
      #   - Sum goals scored/conceded
      #   - Calculate points based on sport rules
      # Sort by: points desc, goal_diff desc, goals_scored desc
      # Return list of dicts with team standings
  ```

#### Views to Create
- [ ] `tournament_leaderboard` - display standings
- [ ] `api_leaderboard` - JSON endpoint for JavaScript

#### Templates to Create
- [ ] `leaderboard.html` - table showing standings
- [ ] Add leaderboard section to `tournament_detail.html`

**Test:** Create multiple matches, verify standings calculate correctly  
**Git Commit:** "Add tournament leaderboard calculation"

---

### ⚡ Phase 8: JavaScript Features (Day 11-12)

#### JavaScript Files to Create (static/js/)
- [ ] `match_submit.js` - AJAX form submission for match results
  ```javascript
  // Fetch API to submit match result
  // Update page without reload
  // Show success/error message
  ```

- [ ] `leaderboard.js` - Dynamic leaderboard updates
  ```javascript
  // Fetch updated standings via API
  // Update table dynamically
  ```

- [ ] `sort_table.js` - Client-side table sorting
  ```javascript
  // Sort MVP tables by clicking headers
  ```

- [ ] `highlight_winner.js` - Visual effects
  ```javascript
  // Add CSS class to winning team
  ```

#### API Views to Create (for JavaScript)
- [ ] `api/match/<id>/submit/` - POST endpoint for match results (returns JSON)
- [ ] `api/tournament/<id>/leaderboard/` - GET standings as JSON
- [ ] Add `@csrf_exempt` or pass CSRF token in JavaScript

#### Updates to Templates
- [ ] Add `<script>` tags to load JavaScript files
- [ ] Add data attributes to HTML elements (e.g., `data-match-id`)
- [ ] Create success/error message divs for JavaScript to update

**Test:** Submit match via AJAX, verify no page reload, leaderboard updates  
**Git Commit:** "Add JavaScript dynamic features"

---

### 🎨 Phase 9: UI Polish (Day 13)

#### Tasks
- [ ] Make all pages responsive (test on mobile)
- [ ] Add Bootstrap cards, badges, alerts
- [ ] Color-code match status (green=completed, blue=scheduled, grey=locked)
- [ ] Add icons (Bootstrap Icons or Font Awesome)
- [ ] Create homepage with links to all features
- [ ] Add breadcrumbs for navigation
- [ ] Style forms with Bootstrap form classes
- [ ] Add loading spinners for AJAX requests
- [ ] Fix any visual bugs
- [ ] Test on different browsers

**Git Commit:** "Polish UI and improve responsiveness"

---

### ✅ Phase 10: Testing & Documentation (Day 14)

#### Testing Checklist
- [ ] Register as each user role
- [ ] Create sport, team, tournament, match
- [ ] Submit match result as referee
- [ ] Add player stats
- [ ] Verify MVP calculation is correct
- [ ] Verify leaderboard is correct
- [ ] Test JavaScript features work
- [ ] Test on mobile device
- [ ] Check all permission restrictions work
- [ ] Test edge cases (tied matches, empty tournaments)

#### Documentation Tasks
- [ ] Write comprehensive README.md
  - [ ] What makes this project distinct
  - [ ] How to run the project
  - [ ] File structure explanation
  - [ ] Features overview
- [ ] Add comments to complex code
- [ ] Document API endpoints
- [ ] Create requirements.txt: `pip freeze > requirements.txt`

#### Video Preparation
- [ ] Script for demo video (under 2 minutes for CS50W)
- [ ] Show all user roles in action
- [ ] Demonstrate JavaScript features
- [ ] Highlight complexity and distinctiveness

**Git Commit:** "Final testing and documentation"

---

## 🚨 Common Mistakes to Avoid

1. **Don't store calculated data** - Winners, MVPs, standings should be computed on-demand
2. **Always check permissions** - Use `@login_required` and custom permission checks
3. **Validate forms** - Check scores are non-negative, teams are in tournament, etc.
4. **Handle edge cases** - What if sport doesn't allow draws but scores are tied?
5. **Test JavaScript** - Use browser console to debug, check Network tab for API calls
6. **Commit regularly** - Don't wait until the end to commit code

---

## 📝 Daily Progress Log

### Day 1: _____/_____
**Completed:**
- [ ] 

**Issues:**
- 

**Tomorrow:**
- 

### Day 2: _____/_____
**Completed:**
- [ ] 

**Issues:**
- 

**Tomorrow:**
- 

_(Continue for all 14 days)_

---

## 🆘 When Stuck - Quick Fixes

**Problem:** Migrations not working  
**Fix:** Delete db.sqlite3, delete migrations folder contents (keep `__init__.py`), run `makemigrations` and `migrate` again

**Problem:** Static files not loading  
**Fix:** Check `STATIC_URL` in settings.py, run `python manage.py collectstatic`, hard refresh browser (Ctrl+Shift+R)

**Problem:** Permission denied errors  
**Fix:** Add `@login_required` decorator, check `request.user.role` in view

**Problem:** JavaScript not working  
**Fix:** Check browser console for errors, verify CSRF token is passed, check API endpoint URL

**Problem:** Foreign key errors  
**Fix:** Make sure related object exists before creating, use `.exists()` to check

---

## 🎯 MVP (Minimum Viable Product)

If running out of time, these features are **essential**:
1. ✅ User roles and authentication
2. ✅ Teams and tournaments
3. ✅ Match result submission
4. ✅ Basic leaderboard calculation
5. ✅ At least 2 JavaScript features (AJAX + one more)

These can be simplified/skipped:
- Join request approval system (just let players join directly)
- Player statistics (focus on match scores only)
- MVP calculation (nice-to-have but not core)
- Extensive UI polish

---

## 📚 Quick Django Commands Reference

```bash
# Start project
django-admin startproject projectname

# Create app
python manage.py startapp appname

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver

# Shell (test queries)
python manage.py shell

# Create requirements file
pip freeze > requirements.txt
```

---

**Remember:** Focus on functionality over perfection. A working app with core features is better than a half-finished complex one! 🚀"# Sports-Tournament-App" 
