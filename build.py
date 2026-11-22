# Builds the five pages of the Linear pitch site into this folder.
# Run: python build.py
import html, os
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
READ = 'November 22, 2026'
D = 'https://linear.app/docs/'
SCHEMA = 'https://github.com/linear/linear/blob/master/packages/sdk/src/schema.graphql'

NAV = [('index.html', 'The proposal'), ('evidence.html', 'The evidence'), ('prototype.html', 'The prototype'), ('how.html', 'How I built it'), ('why.html', 'Why me')]

def page(fn, title, desc, body, script=''):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == fn else '', t) for h, t in NAV)
    out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<meta name="robots" content="noindex,nofollow"><title>%s</title><meta name="description" content="%s">'
           '<link rel="stylesheet" href="assets/site.css"></head><body><a class="skip" href="#main">Skip to content</a>'
           '<div class="flag"><div class="w"><b>Unofficial.</b> A job application for Linear&rsquo;s Product Manager role, built from public pages. Not affiliated with Linear.</div></div>'
           '<header class="w nav"><a class="me" href="index.html"><i></i>Richard J. Valeo</a><nav aria-label="Pages">%s</nav></header>'
           '<main id="main">%s</main>'
           '<footer class="w foot"><span>Richard J. Valeo &middot; Georgetown, Colorado &middot; <a href="https://rjvaleo.github.io/">rjvaleo.github.io</a> &middot; <a href="https://www.linkedin.com/in/rjvaleo">LinkedIn</a></span>'
           '<span>Public pages read on %s. Nothing here comes from inside Linear.</span></footer>%s</body></html>') % (E(title), E(desc), nav, body, READ, script)
    open(os.path.join(HERE, fn), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', fn, len(out))

def a(url, text): return '<a href="%s">%s</a>' % (url, text)
def li(b, span): return '<li><b>%s</b><span>%s</span></li>' % (b, span)

# ---------------------------------------------------------------- the proposal
def row(name, pos=None, label='', none=False):
    if none:
        return '<div class="tlr"><b>%s</b><div class="trk"><span class="dl none" style="left:%d%%">%s</span></div></div>' % (name, pos, label)
    return '<div class="tlr"><b>%s</b><div class="trk"><i class="dm" style="left:%d%%"></i><span class="dl" style="left:%d%%">%s</span></div></div>' % (name, pos, pos, label)

PICTURE = ('<div class="cmp">'
  '<div class="cmpp"><h3>Today</h3><p>Each project makes its own copy. The copies drift.</p>'
  '<div class="tl" role="img" aria-label="Four projects. Three have their own Beta milestone, on three different dates and spelled three ways. The fourth has none.">'
  + row('Sync engine', 44, 'Beta &middot; Oct 23') + row('iOS app', 52, 'Beta 1 &middot; Oct 26') + row('Android app', 61, 'beta &middot; Nov 2') + row('Billing', 30, 'No milestone', none=True)
  + '</div><p class="cap"><b>&ldquo;Are we ready for beta?&rdquo;</b> Open four projects, or keep a spreadsheet.</p></div>'
  '<div class="cmpp"><h3>Proposed</h3><p>One milestone on the initiative. Each project keeps its own slice.</p>'
  '<div class="tl sh" role="img" aria-label="The same four projects sharing one Beta milestone on October 26. Each shows its own progress and what it carried on.">'
  '<div class="shl"><span>Beta &middot; Oct 26</span></div>'
  + row('Sync engine', 52, '3 of 4 &middot; 2 carried on') + row('iOS app', 52, '2 of 4 &middot; 2 carried on') + row('Android app', 52, '2 of 3 &middot; 2 carried on') + row('Billing', 52, '1 of 1 &middot; 1 carried on')
  + '</div><p class="cap"><b>&ldquo;Are we ready for beta?&rdquo;</b> One page. It also says what beta handed to launch.</p></div>'
  '</div>')

def phase(when, title, ships, tags, know):
    return ('<div class="phase"><span class="when">%s</span><h3>%s</h3><p class="note" style="margin-top:10px">%s</p><p>%s</p>'
            '<p class="know"><b>How I will know.</b> %s</p></div>') % (when, title, ships, ''.join('<span class="tag">%s</span>' % t for t in tags), know)

PHASES = ('<div class="four">'
  + phase('First', 'Check the finding', 'A count of initiatives where projects repeat a milestone name, and notes from calls with the leads who run them.', ['Data', 'Customer experience', 'Sales'],
          'I can name five customers who keep this view by hand, and say what is in it.')
  + phase('Then', 'Build the smallest version', 'A shared milestone with a name, a date and a slice per project, plus the carried-over record. Linear&rsquo;s own launches use it first.', ['A designer', 'One or two engineers'],
          'Linear&rsquo;s next launch is reviewed from the milestone, not from a document.')
  + phase('Then', 'Private beta', 'The feature goes to the customers from the first step. I sit in on one milestone review with each.', ['Customer experience', 'Beta customers'],
          'One lead retires the spreadsheet, and tells me what it had that the page lacks.')
  + phase('Last', 'Launch', 'The changelog entry, the docs page and the page for sales, all saying the same thing.', ['Marketing', 'Sales', 'Docs'],
          'Sales uses the page in a live deal and reports the buyer&rsquo;s next question.')
  + '</div>')

INDEX = ('<div class="w hero"><h1>One milestone, many projects.</h1>'
  '<p class="lead">Linear&rsquo;s posting for Product Manager asks for discovery presented with conviction and rigor, messaging that resonates with users, and a sales team that can win with it. This is one finding taken through all three. I built it in one day from Linear&rsquo;s public pages, with AI agents doing the reading.</p>'
  '<div class="bottom"><div><b>The finding</b><span>A launch has one date. In Linear, each project keeps its own copy of the milestone.</span></div>'
  '<div><b>The proposal</b><span>Define the milestone once, on the initiative. Its projects share it, and it shows what each one carried over.</span></div>'
  '<div><b>Done means</b><span>A lead answers &ldquo;are we ready for beta?&rdquo; from one page, and stops keeping the spreadsheet.</span></div></div>'
  '<div class="next"><a class="btn" href="prototype.html">Try the prototype</a><a class="btn ghost" href="evidence.html">Read the evidence</a></div></div>'

  '<section class="w" id="picture"><div class="shead"><div><h2>The same initiative, twice</h2>'
  '<p>A made-up launch with four projects. The numbers on the right match the prototype.</p></div></div>' + PICTURE + '</section>'

  '<section class="w" id="finding"><div class="two"><div><h2>The finding</h2>'
  '<p class="lead">The user is the person leading a launch that spans several projects and has a date that matters.</p>'
  '<p>I do that job now, for ten vendor teams with a date that does not move. So I read Linear&rsquo;s docs the way I would use the product.</p>'
  '<p class="note" style="margin-top:14px">What I cannot see from outside: how many customers repeat a milestone name across projects. Linear can count that in an afternoon. It is the first thing I would ask for.</p></div>'
  '<ul class="plain">'
  + li('Linear&rsquo;s docs say a milestone cannot be shared.', 'The milestones FAQ says it has to be recreated in each project. ' + a(D + 'project-milestones', 'Project milestones, FAQ'))
  + li('The docs describe a workaround.', 'On an initiative you can filter projects by the text of their milestone names. That works while every project spells it the same way. ' + a(D + 'project-milestones', 'Milestones and Initiatives'))
  + li('A customer story shows the review living in a spreadsheet.', 'Sierra&rsquo;s Monday product meeting runs from a sheet that the API refills with milestones, statuses and next steps. Linear tells it as a strength of its API, and it is. It also shows where the cross-project view sits. ' + a('https://linear.app/customers/sierra', 'Sierra'))
  + li('Moves between milestones are recorded, and never added up.', 'The public API records the milestone an issue moved from and to. I found no page in the docs that sums those moves for a milestone. ' + a(SCHEMA, 'API schema'))
  + '</ul></div></section>'

  '<section class="w" id="proposal"><div class="two"><div><h2>What Linear already has</h2><ul class="plain">'
  + li('Milestones with progress, on every plan.', 'Each has a date and a completion percentage, and shows on the timeline.')
  + li('Initiatives that roll projects up.', 'The initiative timeline already shows each project&rsquo;s current milestone.')
  + li('A record of every move.', 'For cycles, the API even keeps the list of what was unfinished at close.')
  + li('Health that goes grey when nobody has reported.', 'It does not stay green. The same rule belongs on a milestone.')
  + '</ul></div><div><h2>The proposal</h2><ul class="plain">'
  + li('Define a milestone once, on an initiative.', 'A name and a date. Any project in the initiative can share it.')
  + li('Each project keeps its slice.', 'Its own issues, progress and lead. Inside the project it is an ordinary milestone, so guests who cannot see initiatives still see it.')
  + li('One line on the initiative timeline.', 'Move the date once and every project follows.')
  + li('Carried over, shown.', 'Each slice shows what arrived from the last milestone and what moved on to the next.')
  + li('Merge what exists.', 'Milestones with the same name become one shared milestone. Nobody starts over.')
  + '</ul></div></div></section>'

  '<section class="w"><div class="two"><div><h2>What I would cut</h2><ul class="plain">'
  + li('A new time box.', 'Linear has cycles for rhythm and milestones for outcomes. A &ldquo;program increment&rdquo; would be a third thing with an invented name.')
  + li('Automatic rollover at the date.', 'A cycle is a rhythm, so it rolls. A milestone is a promise, so a person decides what moves.')
  + li('A locked baseline.', 'Linear keeps scope honest by showing change, not by freezing it.')
  + li('Capacity across teams.', 'A real need, and a different problem.')
  + li('Sign-off at the date.', 'An approval step is busy work until a customer shows me otherwise.')
  + '</ul></div><div><h2>What would change this</h2><ul class="plain">'
  + li('If few initiatives repeat milestone names,', 'the problem is smaller than the FAQ suggests, and I would stop.')
  + li('If Linear already has this under way,', 'I join that work instead of starting it.')
  + li('If leads want carry-over across team cycles more than across milestones,', 'that view goes first. It reads the same record.')
  + li('If customers model phases as sub-initiatives,', 'the shared date belongs there, and this needs no new object at all.')
  + '</ul></div></div></section>'

  '<section class="w" id="steps"><div class="shead"><div><h2>How I would take it from here</h2>'
  '<p>Four steps, each with what ships, who it involves and how I will know. The Linear Method asks for projects that one to three people finish in one to three weeks. I cut the first version with that in mind. Whether it fits is the engineers&rsquo; call.</p></div></div>'
  + PHASES + '</section>'

  '<section class="w" id="message"><div class="shead"><div><h2>The announcement</h2><p>The posting asks for messaging that resonates with users. This is the draft I would bring.</p></div></div>'
  '<div class="card"><span class="when">A draft in the style of Linear&rsquo;s changelog. Written by me. Not a Linear announcement.</span>'
  '<h3>Shared milestones</h3>'
  '<p>A launch has one date, even when five projects are working toward it. You can now define a milestone once on an initiative and share it with the projects that contribute.</p>'
  '<ul><li><b>One name, one date.</b> Change it once and every project follows.</li>'
  '<li><b>Each project keeps its own slice.</b> Its own issues, its own progress.</li>'
  '<li><b>See what carried over.</b> When unfinished work moves to the next milestone, both milestones show it, project by project.</li></ul>'
  '<p>Already have the same milestone in several projects? Merge them into a shared one from the initiative.</p>'
  '<p class="fine" style="margin-top:14px">Why it reads this way: it opens with the user&rsquo;s situation, names one thing, and uses the word Linear already uses. The Method says not to invent terms.</p></div></section>'

  '<section class="w" id="sales"><div class="shead"><div><h2>The page for sales</h2><p>The posting asks for a sales team that can win with customers. This is the page I would hand them.</p></div></div>'
  '<div class="card"><span class="when">A draft for the sales team. Written by me, from public pages.</span>'
  '<h3>Shared milestones, in a deal</h3>'
  '<p><b>When it comes up.</b> A buyer moving from Jira asks how a release across several teams is planned in Linear.</p>'
  '<div class="sales"><div><h4>Say</h4><ul class="plain">'
  '<li>Define the milestone once. Every project on the initiative shares the name and the date.</li>'
  '<li>Each team keeps its own slice and its own lead.</li>'
  '<li>When work moves to the next milestone, Linear shows what moved. Nobody keeps that list by hand.</li></ul>'
  '<h4>Do not say</h4><ul class="plain">'
  '<li>That it is program increment planning. It is a milestone.</li>'
  '<li>That it plans capacity or locks a baseline. It does neither.</li></ul></div>'
  '<div><h4>Questions it answers</h4><ul class="plain">'
  '<li><b>&ldquo;Can we see one date across teams?&rdquo;</b><span>Yes, as one line on the initiative timeline.</span></li>'
  '<li><b>&ldquo;What happens to unfinished work?&rdquo;</b><span>It stays until someone moves it. The move is recorded and shown.</span></li>'
  '<li><b>&ldquo;Can contractors see it?&rdquo;</b><span>In their own project, yes. Initiatives stay hidden from guests, as they are today.</span></li></ul>'
  '<h4>Proof</h4><ul class="plain"><li>None yet. The private beta produces the first customer quote.</li></ul></div></div></div></section>'

  '<section class="w"><div class="two"><div><h2>What I would watch</h2><p class="lead">Linear says it does not use OKRs or run A/B tests. So there is no target here and no experiment.</p>'
  '<p class="note" style="margin-top:12px">Three things to watch, with customers telling me why. I can see no baseline for any of them from outside. ' + a('https://linear.app/now/how-we-hire-at-linear', 'How we hire at Linear') + '</p></div>'
  '<ul class="plain">'
  + li('Shared milestones on initiatives with three or more projects.', 'Use where the problem is, not use overall.')
  + li('Date changes made once.', 'Each one is several edits nobody had to make.')
  + li('Leads who say the spreadsheet is gone.', 'The only one of the three that is the outcome.')
  + '</ul></div>'
  '<div class="next"><a class="btn" href="prototype.html">Use the proposal as a working page</a><a class="btn ghost" href="how.html">How I built this with AI</a></div></section>')

page('index.html', 'One milestone, many projects · Richard J. Valeo',
     'A discovery finding and product proposal for Linear’s Product Manager role, by Richard J. Valeo. Unofficial, built from public pages.', INDEX)

# ---------------------------------------------------------------- the evidence
NF = '<span class="note">Not found</span>'
NR = '<span class="note">Help centre could not be read</span>'
RIV = [
 ('us', 'Linear', D + 'project-milestones', 'Not possible. A milestone is recreated in each project.', 'Cycles and scheduled releases move it on automatically. Milestones do not move.', 'Kept in issue history and the API. No summed view found in the docs.', 'Milestones and initiatives on every plan'),
 ('', 'Jira with Plans', 'https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-roadmaps/', 'A cross-space release lines up several releases on one date.', 'At the end of a sprint the user chooses: backlog, a future sprint or a new one.', 'Sprint and burndown reports list incomplete and removed items, per board.', 'Plans need Premium or Enterprise'),
 ('', 'Jira Align', 'https://www.atlassian.com/software/jira-align', 'A program increment holds every team&rsquo;s sprints.', NF + ' for sprints. A feature belongs to one increment.', 'Points planned against points accepted, by program and increment.', 'A separate product that needs Jira Premium'),
 ('', 'Asana', 'https://asana.com/features/goals-reporting/portfolios', NR, NF, 'A baseline in Gantt view, per project. Source is a 2023 staff post.', 'Portfolios on Advanced and up'),
 ('', 'Shortcut', 'https://www.shortcut.com/help/objectives/objectives-overview/', 'Objectives roll up work across teams. Iterations can belong to one team.', 'An optional automation moves stories to the next iteration, per team.', 'The burndown chart freezes at the end. No list of carried stories found.', 'Iterations on every plan, the automation on paid plans'),
 ('', 'GitHub', 'https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones', 'A milestone belongs to one repository. An iteration field belongs to one project.', 'Moved by hand, in bulk.', NF, 'Not stated on the pages read'),
 ('', 'Azure DevOps', 'https://learn.microsoft.com/en-us/azure/devops/boards/plans/review-team-plans', 'Teams share iteration paths. A delivery plan takes milestone markers.', 'Moved by hand.', 'Velocity keeps the original planned snapshot, per team.', 'Not stated on the pages read'),
]
rows = ''.join('<tr%s><td><b>%s</b></td>%s</tr>' % (' class="us"' if c else '', a(u, n), ''.join('<td>%s</td>' % x for x in cells)) for c, n, u, *cells in RIV)
EVID = ('<div class="w hero"><h1>The evidence.</h1><p class="lead">Everything on this site comes from pages any visitor can open, read on ' + READ + '. I created no account, submitted no form and did not open the Linear app.</p></div>'
  '<section class="w"><h2>Where Linear already leads</h2><ul class="plain">'
  + li('Unfinished work moves on by itself, and the record is kept.', 'Cycles roll open issues into the next cycle. The closed cycle keeps its totals as they were, and the API keeps the list of what was unfinished at close. ' + a(D + 'use-cycles', 'Cycles') + ', ' + a(SCHEMA, 'API schema'))
  + li('Missing information is shown as missing.', 'A project whose update is overdue goes grey. It does not stay green. I hold my own planning board to the same rule: a gate with no data shows a dash. ' + a(D + 'initiative-and-project-updates', 'Updates'))
  + li('Scope change is shown, not frozen.', 'A filter separates work planned for a cycle from work added after it started. The project graph draws scope over time and predicts a date with a range. ' + a(D + 'filters', 'Filters') + ', ' + a(D + 'project-graph', 'Project graph'))
  + li('One model on every plan.', 'Issues, projects, cycles and initiatives are included on the free plan. The paid plans add structure around them. ' + a('https://linear.app/pricing', 'Pricing'))
  + li('Agents already work on plans.', 'Linear Agent drafts project updates from recent changes, and Loops respond to changes in initiatives, projects and cycles. ' + a('https://linear.app/changelog/2026-06-18-agent-assisted-project-updates', 'June 2026') + ', ' + a('https://linear.app/changelog/2026-09-14-loops-for-product-management', 'September 2026'))
  + '</ul></section>'
  '<section class="w"><div class="shead"><div><h2>Linear beside six rivals</h2><p>What each vendor&rsquo;s own pages say about planning above one team. Each name links to one of that vendor&rsquo;s pages.</p></div></div>'
  '<div class="tw"><table><thead><tr><th>Vendor</th><th>One date shared across projects or teams</th><th>Unfinished work at the boundary</th><th>A record of what moved on</th><th>Where it sits</th></tr></thead><tbody>' + rows + '</tbody></table></div>'
  '<p class="note" style="margin-top:14px">&ldquo;Not found&rdquo; means not found on the pages read, not that the vendor lacks it. An AI research agent gathered the rival rows from each vendor&rsquo;s own pages and re-checked its wording against saved text. I checked the Linear row against saved page text, and I have not checked the rival rows line by line. The help centres of Jira Align and Asana could not be read, so those two rows are thinner.</p>'
  '<p class="note" style="margin-top:10px">What the table says: the rivals that share a date across teams do it with a heavier object, a release plan or a program increment. Linear can do it with the milestone it already has.</p></section>'
  '<section class="w"><div class="two"><div><h2>What a proposal to Linear has to respect</h2><p class="lead">Linear publishes how it builds. A proposal that ignores it is not a proposal for Linear.</p></div><ul class="plain">'
  + li('Do not invent terms.', 'The Method says projects should be called projects. So this is a milestone, not a program increment. ' + a('https://linear.app/method/introduction', 'Linear Method'))
  + li('Say no to busy work.', 'Nothing new to fill in. The carried-over record comes from moves Linear already keeps.')
  + li('Build for the creators, not for perfect reports.', 'The page is for the lead who has to decide. It costs the people doing the work nothing.')
  + li('No OKRs and no A/B tests.', 'So the test is customers and judgment. ' + a('https://linear.app/now/how-we-hire-at-linear', 'How we hire at Linear'))
  + li('Small projects.', 'One to three people, one to three weeks. The first version is cut to be small. ' + a('https://linear.app/method/scope-projects', 'Scope projects down'))
  + '</ul></div></section>'
  '<section class="w"><div class="two"><div><h2>What is not on this page</h2></div><div><p>While reading, I found a handful of places where Linear&rsquo;s public pages disagree with each other, two links that no longer resolve, and some small slips. None is serious.</p>'
  '<p>Those are in a short findings report I will send to Linear directly. A public page is the wrong place for them.</p>'
  '<div class="next"><a class="btn" href="index.html">Back to the proposal</a><a class="btn ghost" href="how.html">How the research was run</a></div></div></div></section>')
page('evidence.html', 'The evidence · Richard J. Valeo', 'What Linear’s public pages say about planning above one team, beside six rivals, with sources.', EVID)

# ---------------------------------------------------------------- how
def step(who, cls, title, text): return '<div class="step"><span class="who %s">%s</span><b>%s</b><span>%s</span></div>' % (cls, who, title, text)
HOW = ('<div class="w hero"><h1>How I built this.</h1><p class="lead">I ran this with Claude as my lead agent. AI agents did the research and built the pages. Here is the workflow, what was checked, and where the AI was wrong.</p></div>'
  '<section class="w"><h2>The workflow</h2><div class="flow">'
  + step('Me', 'me', 'Set the approach', 'Pitch the role with a plan and a working prototype. Read the company as its user would before pitching anything.')
  + step('AI', 'ai', 'Read everything public', 'One agent on Linear: 654 pages saved, with 105 documentation pages, 255 changelog entries and the public API schema. A second agent on six rivals.')
  + step('AI', 'ai', 'Check each finding', 'Every claim about Linear was checked against the saved page text. The starting idea did not survive the check.')
  + step('AI', 'ai', 'Build', 'The proposal, the prototype and a private findings report.')
  + step('Me', 'me', 'Read it and stand behind it', 'I read every page of this site before sending it.')
  + '</div><p class="note" style="margin-top:16px">The lead agent was Claude. It ran the research, did the checking and wrote the pages. One working day, ' + READ + '.</p></section>'
  '<section class="w"><div class="two"><div><h2>The rules the agents worked under</h2><ul class="plain">'
  + li('Every claim carries its source.', 'A page address and where on the page. The page text is saved, so any claim can be checked again.')
  + li('&ldquo;Not found&rdquo; is never rewritten as &ldquo;missing&rdquo;.', 'The agents had to say where they looked. Only a statement by Linear itself counts as confirmed absent.')
  + li('Read only.', 'No account, no login, no form, no testing of any system. Nobody opened the Linear app.')
  + li('Separate agents for Linear and for rivals.', 'So what one vendor says about another never stood in for that vendor&rsquo;s own page.')
  + '</ul></div><div><h2>Where the AI was wrong or thin</h2><ul class="plain">'
  + li('The starting idea was wrong.', 'The research began by looking for missing cross-team sprint planning. Linear&rsquo;s sub-teams already share one cycle schedule. The proposal moved to the gap Linear&rsquo;s own FAQ confirms.')
  + li('One claim could not be settled, so it was cut.', 'An early draft said no screen shows what a closed cycle handed on. A 2020 changelog line suggests the app does show it. Without opening the app there is no way to know.')
  + li('The demand evidence is thin.', 'Linear has no public forum that the agents could read. The case rests on Linear&rsquo;s own FAQ and one customer story, not on customer requests.')
  + li('The rival rows are thinner than the Linear row.', 'Two help centres could not be read, and the rows were not checked line by line. The evidence page says so.')
  + '</ul></div></div></section>'
  '<section class="w"><div class="two"><div><h2>Where my judgment came in</h2><p class="lead">The agents can read 650 pages in an hour. They cannot decide what a hiring team should be shown.</p></div><ul class="plain">'
  + li('Pitch with a plan and a working prototype.', 'Linear&rsquo;s hiring page says the best talker is not always the best doer. A page you can use is the doing.')
  + li('Read the company as its user would, before pitching anything.', 'The lens here is my own job: ten vendor teams and a date that does not move.')
  + li('Report what turned up, privately.', 'If I find holes, I bring them up. The findings went into a report, not onto this site.')
  + li('Say what I cannot see.', 'The proposal has a section on what would change it, because I have no view of Linear&rsquo;s data or its roadmap.')
  + li('Stand behind the output.', 'I read every page of this site before sending it. If something here is wrong, that is mine, not the agent&rsquo;s.')
  + '</ul></div>'
  '<div class="next"><a class="btn" href="why.html">Why me</a><a class="btn ghost" href="index.html">Back to the proposal</a></div></section>')
page('how.html', 'How I built this · Richard J. Valeo', 'The AI workflow behind this proposal, what was checked, and where judgment came in.', HOW)

# ---------------------------------------------------------------- why me
def trow(ask, have): return '<tr><td><b>%s</b></td><td>%s</td></tr>' % (ask, have)
PF = 'https://rjvaleo.github.io/'
WHY = ('<div class="w hero"><h1>Why me.</h1><p class="lead">I have never held the title Product Manager. I started as a front-end developer, and today I am the product owner and builder of my own products and of the tools a ten-team program plans from.</p></div>'
  '<section class="w"><h2>What the posting asks, and what I have done</h2><div class="tw"><table><thead><tr><th style="width:32%">The posting asks for</th><th>What I have done</th></tr></thead><tbody>'
  + trow('Previous experience in engineering and/or design roles', 'I started as an interface engineer at Organic, as a front-end developer on Bloomingdale&rsquo;s first e-commerce site, then spent three years as a web developer. I build again now, with AI agents, in Rust, TypeScript and C++.')
  + trow('Up-front discovery through user interviews, competitive research and data analysis', 'Before planning my current program I interviewed every workstream lead, and turned the answers into one script that ten vendor teams now plan from. Earlier I planned, ran and presented a user-testing study of a Toyota dealer site. ' + a(PF + 'case-pi-dashboard.html', 'Case study'))
  + trow('Findings presented with conviction and rigor', 'The planning board I built never shows a number it cannot source, and a gate with no data shows a dash, never green. I check my agents&rsquo; numbers too: a reported 682 tests turned out to be 384.')
  + trow('Helping engineers and designers understand user needs', 'I write it down before anyone builds. Six design documents for the requirements app I co-built, and for the planning module: research, a gap analysis, open decisions and a mock-up before any code. ' + a(PF + 'case-rtm-tool.html', 'Case study'))
  + trow('Messaging around upcoming features', 'Eight years as an agency producer. I led the design, UX and information architecture teams through the sitemap, wireframes and copy deck for American Express OPEN, and produced a film for Citi that sold a website before a line of it was built. ' + a(PF + 'case-jack-morton.html', 'Case study'))
  + trow('Enabling sales and marketing to win', 'I created, pitched and presented concepts to Citibank and American Airlines, with proposals and cost estimates, and sat on an agency proposal team. On my current program I ran the two-day close-out roadshow for the client.')
  + trow('Design and product taste', 'Judge it from the prototype on this site and from the products I ship. On one of them I ran a three-stage design review that took clipped controls from 17 to 0. ' + a('prototype.html', 'Prototype') + ', ' + a(PF + 'case-idm.html', 'idM'))
  + trow('Exceptional product and operational judgement', 'I keep decisions of record and reverse them in the open. I built a sixth audio engine, cut it the same day and kept the write-up. I switched an engine from Rust to C++ a day and a half in, and wrote down why. ' + a(PF + 'case-audio-edit-tag.html', 'Case study'))
  + trow('Extreme speed and clarity', 'A browser music product went from first commit to public alpha in four days. The planning board was a working prototype in five weeks. This site took one day.')
  + trow('Shameless curiosity', 'I rebuilt a classic composing program from its manual alone, by turning the manual into 180 capabilities with a test for each.')
  + trow('Teams and agents', 'Four music products shipped with AI agents, with specs written before code and tests as the referee. I also run a loop where local models work coding jobs against hidden tests. ' + a(PF + 'how-i-work.html', 'How I work'))
  + '</tbody></table></div></section>'
  '<section class="w"><div class="two"><div><h2>The gap, plainly</h2></div><div><p class="lead">I have not worked at a product-led software company of Linear&rsquo;s kind, and my titles have been Scrum Master, Agile Coach and Release Train Engineer.</p>'
  '<p>My product work is on my own products and on tools inside a program. I have not owned a feature with a sales team waiting on the message.</p>'
  '<p>What I have done is the work in the posting&rsquo;s four bullets at a smaller size: ask the users, write it down, build it, and explain it to the people who have to adopt it. I have also lived the problem on this site from the other side, running multi-team programs in Jira.</p>'
  '<p>Linear&rsquo;s hiring page says it values slope over credentials. This site is my evidence of slope: one finding, taken from reading to a working page, in a day.</p>'
  '<div class="next"><a class="btn" href="https://rjvaleo.github.io/">See my work</a><a class="btn ghost" href="https://www.linkedin.com/in/rjvaleo">LinkedIn</a></div></div></div></section>')
page('why.html', 'Why me · Richard J. Valeo', 'Richard J. Valeo’s record against Linear’s Product Manager role.', WHY)

# ---------------------------------------------------------------- prototype (markup here, behaviour in assets/proto.js)
PROTO = open(os.path.join(HERE, '_proto.html'), encoding='utf-8').read()
page('prototype.html', 'Shared milestones prototype · Richard J. Valeo', 'A clickable prototype of milestones shared across projects, with what each one carried over. Sample data.', PROTO, '<script src="assets/proto.js"></script>')
