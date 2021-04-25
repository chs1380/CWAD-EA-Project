from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import current_app, db
from app.main.forms import EditProfileForm, PostForm, NewReply, EditPostForm
from app.models import User, Post, Comment
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(category_id=form.category.data, title=form.title.data, body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('已出post'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('casual.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/casual')
def casual():
    page = request.args.get('page', 1, type=int)
    if post:
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.casual', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.casual', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('casual.html', title=_('Casual'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/relationship', methods=['GET', 'POST'])
def relationship():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.relationship', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.relationship', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('relationship.html', title=_('Relationship'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/blackhole', methods=['GET', 'POST'])
def blackhole():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.blackhole', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.blackhole', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('blackhole.html', title=_('Blackhole'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, current_user, login_required

@bp.route('/post/<post_id>', methods=['GET', 'POST'])
# @login_required
# def comment(post_id):
#     form = NewReply()
#     if form.validate_on_submit():
#         comment = Comment(body=form.post.data, author=current_user)
#         db.session.add(comment)
#         db.session.commit()
#         flash(_('Your comment is now live!'))
#         return redirect(url_for('main.casual'))
#     page = request.args.get('page', 1, type=int)
#     posts = current_user.followed_posts().paginate(
#         page, current_app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('main.casual', page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('main.casual', page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('casual.html', title=_('Casual'), form=form,
#                            posts=posts.items, next_url=next_url,
#                            prev_url=prev_url)
def post(post_id):
    form = NewReply()
    post = Post.query.get(int(post_id))
    if form.validate_on_submit():
        comment = Comment(body=form.message.data, timestamp=datetime.now())
        post.comment.append(comment)
        db.session.commit()
    comment = Comment.query.filter_by(post_id=post_id).all()
#    post_category = Post.query.get(int(post.category))
#    post = Post.query.filter_by(category=post_category)
   # qry = db.session.query(post.category).filter(post.category==post.category)
    # print('debug')
    # print(comment[0].body)
    # print(post)
   # return render_template('post.html', qry=qry, post=post, form=form, comments=comment, current_user=current_user)
    return render_template('post.html', post=post, form=form, comments=comment, current_user=current_user)
# def filterpost(category_id):
#    body = Post.query.filter_by(category_id=category_id).(User.name.in_(['input_id_1', ''])).all()
# def get_post_id(post_id):
#   return post_id
# @app.template_filter('filterpost')
# def filterpost(body, category_id='1'):
#    return body.category(category_id)
    #
    # form = NewReply()
    #
    # post = Post.query.get(int(post_id))
    #
    # if form.validate_on_submit():
    #     comment = Comment(body=form.comment.data, author=current_user)
    #     post.replies.append(comment)
    #     db.session.commit()
    #
    # comment = Comment.query.filter_by(post_id=post_id).all()
    #
    # return render_template('post.html', post=post, form=form, comment=comment, current_user=current_user)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('你嘅修改可以儲存.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/edit_post', methods=['GET', 'POST'])
@login_required
def edit_post():
    form = EditPostForm(current_user.username)
    if form.validate_on_submit():
        Post.body = form.post.body
        db.session.commit()
        flash(_('你嘅修改已儲存.'))
        return redirect(url_for('main.edit_profile'))
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('搵唔到User %(username)s.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('你冇得follow你自己!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('追蹤緊 %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('搵唔到User %(username)s.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('你冇得follow你自己!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('追蹤緊 %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))
