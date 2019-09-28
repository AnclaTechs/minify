# Bug reports and Suggestions
Bug reports and feature suggestions can be submitted to [GitHub Issues](https://github.com/olamigokayphils/minify/issues). Please make sure that you are not submitting duplicates, and that a similar report or request has not already been resolved or rejected in the past using the search function. Please also use descriptive, concise titles.

**How to Write a Bug report**
- Please add as much information as possible, for example
    - browser(s) and version(s), is the problem reproducible on different clients
    - Logfiles if available
    - steps to reproduce
    - what you expected to happen
    - what actually happened

# Contributing Content

Thank you for considering contributing to Minify. You are welcome to contribute code to Minify in order to fix bugs or to implement new features.

There are three important things to know:

1. You must be aware of the Apache License (which describes contributions) and **agree to the Contributors License Agreement**. This is common practice in all major Open Source projects. For company contributors special rules apply. See the respective section below for details.

2. There are **several requirements regarding code style, quality, and product standards** which need to be met (we also have to follow them). The respective section below gives more details on the coding guidelines.

3. **Not all proposed contributions can be accepted.** Some features may e.g. just fit a third-party add-on better. The code must fit the overall direction of Minify and really improve it. The more effort you invest, the better you should clarify in advance whether the contribution fits: the best way would be to just open an issue to discuss the feature you plan to implement (make it clear you intend to contribute).

# Contributor License Agreement (CLA)
When you contribute (code, documentation, or anything else), you have to be aware that your contribution is covered by the same [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0) that is applied to Minify itself. In particular you need to agree to the Individual Contributor License Agreement, which can be [found here](https://cla-assistant.io/AnclaTech/minify). (This applies to all contributors, including those contributing on behalf of a company). If you agree to its content, you simply have to click on the link posted by the Minify CLA assistant as a comment to the pull request. Click it to check the CLA, then accept it on the following screen if you agree to it. The CLA assistant will save this decision for upcoming contributions and will notify you if there is any change to the CLA in the meantime.

# Company Contributors
If employees of a company contribute code, in **addition** to the individual agreement above, there needs to be one company agreement submitted. This is mainly for the protection of the contributing employees.

A company representative authorized to do so needs to download, fill, and print the [Corporate Contributor License Agreement](/CCLA.pdf) form. Then, Scan it and e-mail it to [olamigokayphils@gmail.com](olamigokayphils@gmail.com).


# Contributing content guideline

**Coding Style**
- Do write comments. (You don't have to comment every line, but if you come up with something that's a bit complex/weird, just leave a comment. Bear in mind that you will probably leave the project at some point and that other people will read your code. Undocumented huge amounts of code are worthless!)
- Indentation:JS/CSS: 2 spaces; HTML: 4 spaces; **Python: Tabs**;
- Don't overengineer. Don't try to solve any possible problem in one step, but try to solve problems as easy as possible and improve the solution over time!
- Do generalize sooner or later! (if an old solution, quickly hacked together, poses more problems than it solves today, refactor it!)
- Keep it compatible. Do not introduce changes to the public API, db schema or configurations too lightly. Don't make incompatible changes without good reasons!
- If you do make changes, document them! (see below)

# Braching Model/git workflow
see git flow: [http://nvie.com/posts/a-successful-git-branching-model/](http://nvie.com/posts/a-successful-git-branching-model/)

**``master`` branch**
- The stable
- This is the branch everyone should use for production stuff.

**``develop`` branch**
- Everything that is READY to go into master at some point in time
- This stuff is tested and ready to go out.

**release branches**
- Changes that should go into master very soon
- only bugfixes go into these (see [http://nvie.com/posts/a-successful-git-branching-model/](http://nvie.com/posts/a-successful-git-branching-model/) for why)
- We should not be blocking new features to develop, just because we feel that we should be releasing it to master soon. This is the situation that release branches solve/handle.

**hotfix branches**
- Fixes for bugs in master

**feature branches (in your own repos)**
- These are the branches where you develop your features in
- If it's ready to go out, it will be merged into develop


