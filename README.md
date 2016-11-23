### A Simple Flask Blog

This is a simple Flask Blog, as seen in the [Fromzero](https://www.udemy.com/python-flask-course/) course.

Get support in our chat room: [![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?maxAge=2592000)](https://gitter.im/fromzeroedu/flask_blog_c9)



########################################################################################

Here is what I have changed, probably not an all inclusive list:

1. Even though setup blog is a one time thing I polished it a little.
    - If you are signed into an author account when you go to setup it just takes
      that information rather than creating another new author
2. Implemented the comments in the blog posts per the assignment. The comments are paginated on each individual post page. 
3. Replaced the is_author system with two new decorators, author_of_this and right_author. Everyone who makes an account is now potentially an author
   
   -author_of_this is to decorate view fcns that handle editing objects (comments and posts) with a particular author
   (and therefore these objects must have an author_id member) it check the object author_id against session author.id 
   to ensure that whoever in logged in only edits thier objects
   
   -right_author is very similar but used to filter who can edit the author profiles/ profile pages (these were implemented next) 
4. Implemented author profile picture that show up with the comments of the author.
5. Admin page functionality was replaced with a combination of beefing up the indx page and implementing new author_page. 
    - From the index page you can now create a new blog post.
    - The author_page is basically a vastly simplified facebook page. The author's picture is there and a paginated list of that author's posts
      are there as well. This page utilizes the hyperlinks that we created earlier in the posts. Further if an author looks at thier own profile there is 
      a hyperlink which allows the user to edit their profile, just like the post_edit stuff we did earlier. So there is a kind of double layer of security 
      against unauthorized editing of someone elses account, first the hyperlink wont show up for the wrong author, but if they go directly 
      to the url they are 403'd from the new decorators.
      

   