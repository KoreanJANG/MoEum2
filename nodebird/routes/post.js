const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const { Post, Hashtag, Comment } = require('../models');
const { isLoggedIn } = require('./middlewares');

const router = express.Router();

try {  // 업로드 폴더 생성  
  fs.readdirSync('uploads');
} catch (error) {
  console.error('uploads 폴더가 없어 uploads 폴더를 생성합니다.');
  fs.mkdirSync('uploads');
}

// 이미지 업로드 처리 부분
const upload = multer({
  storage: multer.diskStorage({
    destination(req, file, cb) {
      cb(null, 'uploads/');  // 업로드 폴더에 이미지를 저장하겟다 
    },
    filename(req, file, cb) {
      const ext = path.extname(file.originalname);
      cb(null, path.basename(file.originalname, ext) + Date.now() + ext);
    },
  }),
  limits: { fileSize: 5 * 1024 * 1024 },
});

router.post('/img', isLoggedIn, upload.none(), (req, res) => {  // 이미지가 반드시 들어가지 않아도 처리되게 수정 
  console.log(req.file); // 위의 구문을 해석하면, post('/img'로 로그인한사람이 요청하면 업로드 한다 
  res.json({ url: `/img/${req.file.filename}` });  // 업로드가 완료되면 /img/${req.file.filename} 이것을 프론트로 돌려보내준다 
});                                             // 이것은 게시글에도 같이 적용된다 

// 게시글 업로드 부분
const upload2 = multer();
router.post('/', isLoggedIn, upload2.none(), async (req, res, next) => { 
  try {
    console.log(req.user);
    const post = await Post.create({ // await가 있으면 위에 반드시 async가 있어야 한다 
      content: req.body.content, // 업로드가 없다. 옆에 3줄의 바디들만 올라간다 
      img: req.body.url,
      UserId: req.user.id,
      Type: req.body.type, // 여기서부터 우리꺼다. 우리가 브라우저를 통해 보여줄 데이터인데. 여기 라우터를 타고 입력된다.
      Distributor: req.body.Distributor,
      Publisher: req.body.publisher,
      Thumbnail_image: req.body.Thumbnail_image,
      User_url: req.body.User_url,
      Title: req.body.Title
    });
    const hashtags = req.body.content.match(/#[^\s#]*/g);
    if (hashtags) {
      const result = await Promise.all(
        hashtags.map(tag => {
          return Hashtag.findOrCreate({
            where: { title: tag.slice(1).toLowerCase() },
          })
        }),
      );
      await post.addHashtags(result.map(r => r[0]));
    }
    res.status(200).send(post);
  } catch (error) {
    console.error(error);
    next(error);
  }
});

/**
 * 공개 여부를 변경하는 API
 */
router.post('/change/public', isLoggedIn, async (req, res) => {
  const postId = req.body.id;
  const isPublic = req.body.isPublic;

  await Post.update({
    Public: isPublic
  }, {
    where: {
      id: postId
    }
  });

  res.sendStatus(200);
});

router.post('/delete', isLoggedIn, async (req, res) => {
  // 삭제할 게시물 아이디를 파라미터에서 가져온다.
  const postId = req.body.id;
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;

  const post = await Post.findByPk(postId);
  // 글 작성자가 아니면 에러를 발생시킨다.
  if (post.UserId !== userId) {
    res.status(500).send({ message: '글 작성자만 삭제할 수 있습니다.' });
    return;
  }

  // 글을 삭제시킨다. (deletedAt에 날짜만 넣어진다.)
  await post.destroy();
  res.sendStatus(200);
});

/**
 * 댓글 등록
 */
router.post('/comment', isLoggedIn, async (req, res) => {
  // 댓글 등록할 게시물 아이디
  const postId = req.body.postId;
  // 댓글내용
  const comment = req.body.comment;
  // 로그인 사용자 아이디
  const userId = req.session.passport.user;

  // 코멘트 생성
  await Comment.create({
    userId: userId, // 작성자 유저 아이디
    postId: postId, // 코멘트 달릴 게시물 아이디
    content: comment // 코멘트 내용
  });

  res.sendStatus(200);
});

/**
 * 대댓글 입력
 */
router.post('/comment/child', isLoggedIn, async (req, res) => {
  // 게시물 아이디
  const postId = req.body.postId;
  // 대댓글 다는 댓글 아이디
  const parentCommentId = req.body.parentCommentId;
  // 코멘트 내용
  const comment = req.body.comment;
  // 로그인 아이디
  const userId = req.session.passport.user;

  // 대댓글 내용 저장
  await Comment.create({
    userId: userId, // 작성자 유저 아이디
    postId: postId, // 코멘트 달릴 게시물 아이디
    content: comment, // 코멘트 내용
    parentId: parentCommentId // 대댓글의 경우 대댓글의 부모 댓글 아이디
  });

  res.sendStatus(200);
});

router.post('/comment/delete', /*isLoggedIn,*/ async (req, res) => {
  const commentId = req.body.commentId;
  const loginUserId = req.session.passport.user;

  // 댓글아이디로 댓글을 조회한다.
  const comment = await Comment.findByPk(commentId);
  // 댓글이 속한 글을 가져온다.
  const post = await comment.getPost();
  // 코멘트가 자신이 썼거나 아니면 트윗글이 자신의 것일때만 삭제가 가능함.
  if (comment != null && comment.userId === loginUserId || post.UserId === loginUserId) {
    await comment.destroy();
    res.sendStatus(200);
  } else {
    res.status(400).send({message: '댓글 삭제를 실패하였습니다. 자신의 글만 삭제가능합니다.'});
  }
});

module.exports = router;
