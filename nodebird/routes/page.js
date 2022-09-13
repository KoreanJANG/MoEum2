const express = require('express');
const { isLoggedIn, isNotLoggedIn } = require('./middlewares');
const { Post, User, Hashtag, Comment, Like, Trend, Question, Declareban} = require('../models');
const Sequelize = require('sequelize');
const Op = Sequelize.Op;
const { makePaginate } = require('sequelize-cursor-pagination');


const router = express.Router();

router.use((req, res, next) => {  // 팔로잉 구현 부분
  res.locals.user = req.user;
  res.locals.followerCount = req.user ? req.user.Followers.length : 0;
  res.locals.followingCount = req.user ? req.user.Followings.length : 0;
  res.locals.followerIdList = req.user ? req.user.Followings.map(f => f.id) : [];
  next();
});

router.get('/profile', isLoggedIn, (req, res) => {  // profile.html에서 들어오면 얘가 받는다 
  res.render('profile', { title: '내 정보 - NodeBird' });
});

/**
 * 내 컨텐츠 목록 라우터
 */
router.get('/mycontents', isLoggedIn, async (req, res) => {  
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;
  const sort_field = req.body.sort_field;
  const sort_rule = req.body.sort_rule;
  const offset = req.body.offset;
  const limit = req.body.limit;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const posts = await Post.findAll({
    include: {
      model: User,
      attributes: ['id', 'nick'],
      where: {
        id: userId, // 로그인한 사용자의 컨텐츠만 가져오도록 조건절을 넣어준다.
      }
    },
    order: [[sort_field, sort_rule]], // 프론트로부터 정렬 정보를 받는다
    offset: offset,
    limit: limit, 
  });

  res.status(200).send(posts)
  // res.render('mycontents', {
  //   title: '내 컨텐츠 - NodeBird',
  //   twits: posts,
  // });
});

/**
 * 내 질문보기 라우터
 */
 router.get('/myquestion', isLoggedIn, async (req, res) => {  
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;
  const offset = req.body.offset;
  const limit = req.body.limit;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const questions = await Question.findAll({
    include: {
      model: User,
      attributes: ['id', 'nick'],
      where: {
        id: userId, // 로그인한 사용자의 컨텐츠만 가져오도록 조건절을 넣어준다.
      }
    },
    where: {
      Public: true // 공개된 게시물만 출력시킨다.
    },
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
    offset: offset,
    limit: limit, 
  });

  res.status(200).send(questions)
  // res.render('mycontents', {
  //   title: '내 컨텐츠 - NodeBird',
  //   twits: questions,
  // });
});

/**
 * 내 댓글보기 라우터
 */
 router.get('/mycomments', isLoggedIn, async (req, res) => {  
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;
  const offset = req.body.offset;
  const limit = req.body.limit;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const comments = await Comment.findAll({
    include: {
      model: User,
      attributes: ['id', 'nick'],
      where: {
        id: userId, // 로그인한 사용자의 컨텐츠만 가져오도록 조건절을 넣어준다.
      }
    },
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
    offset: offset,
    limit: limit, 
  });

  res.status(200).send(comments)
  // res.render('mycontents', {
  //   title: '내 컨텐츠 - NodeBird',
  //   twits: comments,
  // });
});


/**
 * 내가 좋아요 누른 컨텐츠 불러오기
 */
 router.get('/mylikes', isLoggedIn, async (req, res) => {  
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const userId = req.session.passport.user;
  const offset = req.body.offset;
  const limit = req.body.limit;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const questions = await Question.findAll({
    include: [
    {
      model: User,
      attributes: ['id', 'nick'],
      // where: {
      //   id: userId, // 로그인한 사용자의 컨텐츠만 가져오도록 조건절을 넣어준다.
      // }
    },
    {
      model: Like,
      attributes: ['id', 'like', 'userId'],
      where: {
        like: true, // 라이크가 트루 인것만 가져온다.
        userid: userId, 
  }}],
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
    offset: offset,
    limit: limit, 
  });

  res.status(200).send(questions)
  // res.render('mycontents', {
  //   title: '내 컨텐츠 - NodeBird',
  //   twits: comments,
  // });
});

/**
 * 다른사람 질문한거 보기
 */
 router.get('/other/public', isLoggedIn, async (req, res) => {  
  // 프론트로부터 userid값을 받는다 
  const userId = req.body.userId;;  // !!웹에서 테스트안된다...하지만 값을 강제입력시키면된다!
  const offset = req.body.offset;
  const limit = req.body.limit;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const questions = await Question.findAll({
    include: {
      model: User,
      attributes: ['id', 'nick'],
      where: {
        id: userId,
      }
    },
    where: {
        Public: true, // 공개된 게시물만 출력시킨다.
    },
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
    offset: offset,
    limit: limit, 
  });
  res.status(200).send(questions)
});

/**
 * 다른사람 댓글보기  ====> 일단 여기에 신고차단을 테스트 할 것이다. 
 */
 router.get('/other/comments', isLoggedIn, async (req, res) => {  
  // 로그인 세션에서 로그인 사용자 아이디를 가져온다.
  const searchId = req.body.searchId;
  const offset = req.body.offset;
  const limit = req.body.limit;
  const loginUserId = req.session.passport.user;
  // 로그인한 사용자의 게시물만 조회해서 가져온다.
  const comments = await Comment.findAll({
    include:[ 
      {
        model: User,
        attributes: ['id', 'nick'],
        where: {
          id: searchId, // 찾으려고 하는 사용자의 것만 불러온다 
        }
      },
      // {
      //   model: Declareban,
      //   where: {
      //     userId: loginUserId
      //     }
      // },
  ],    
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
    offset: offset,
    limit: limit,    
  });
  res.status(200).send(comments)
});


router.get('/join', isNotLoggedIn, (req, res) => {  // join.html에서 들어오면 얘가 받는다 
  res.render('join', { title: '회원가입 - NodeBird' });
});

// 질문하기 전체보기 
router.get('/', async (req, res, next) => { // Post.findAll로 해서 업로드된 게시글들을 찾고
  const offset = req.body.offset;
  const limit = req.body.limit;
  try {
    const questions = await Question.findAll({
      include: [
        {
          model: User,
          attributes: ['id', 'nick'],
        },
        {
          model: Like,
          required: false,
          attributes: ['like'],
        },
        {
          model: Comment, // 댓글도 게시물을 가져올때 같이 가져온다. -> post.Comments 로 접근한다.
          required: false, // 댓글이 게시물에 존재하지 않을수 있으므로 false로 설정한다.
          where: {
            parentId: { // parentId가 없는 댓글은 대댓글이 아니므로 parentId 가 null인 글만 가져온다.
              [Op.eq]: null
            }
          },
          include: [
            {
              model: User, // 댓글 작성자를 알기위해 댓글을 작성한 사용자 정보를 가져온다.
              attributes: ['userid'], // User테이블에서 userid만 조회한다.
            },
            {
              model: Comment, // 댓글의 댓글(대댓글)을 가져오기 위한 댓글에 속한 댓글을 가져온다.
              include: {
                model: User, // 대댓글을 작성한 사용자의 정보를 가져온다.
                attributes: ['userid'], // User테이블에서 userid만 조회한다.
              }
            },
          ]
        },
      ],
      where: {
        Public: true // 공개된 게시물만 출력시킨다.
      },
      order: [
        ['updatedAt', 'DESC'], // 글 작성 최신순. 소트_필드, 소트_룰 을 프론트로 부터 받는다 
        [Comment, 'createdAt', 'DESC'], // 댓글 작성 최신순
        [Comment, Comment, 'createdAt', 'DESC'], // 대댓글 작성 최신순
      ],
      offset: offset,
      limit: limit,
      // order: [
      //   [sort_field, sort_rule], // 프론트로부터 글의 정렬의 기준과 방법을 받는다 
      //   [Comment, sort_field, sort_rule], // ?? 댓글은 그냥 시간순이지 않나??
      //   [Comment, Comment, sort_field, sort_rule], // 대댓글도 마찬가지 
      // ],
    });

    res.status(200).send(questions)
    // res.render('main', {
    //   title: 'NodeBird',
    //   twits: questions,  // 찾은 게시물들은 twits로 넣어준다
    //   loginUserId: req.session.passport ? req.session.passport.user : null // 현재 로그인한 유저 아이디를 세션에서가져와 view로 전달한다.
    // });
  } catch (err) {
    console.error(err);
    next(err);
  }
});


// 댓글 대댓글만 불러오는 라우터 => 현재 이것은 안쓴다 
router.get('/comment', async (req, res, next) => { // Post.findAll로 해서 업로드된 게시글들을 찾고
  try {
    const questions = await Question.findAll({
      include: [
        {
          model: User,
          attributes: ['id', 'nick'],
        },
        {
          model: Comment, // 댓글도 게시물을 가져올때 같이 가져온다. -> post.Comments 로 접근한다.
          required: false, // 댓글이 게시물에 존재하지 않을수 있으므로 false로 설정한다.
          where: {
            parentId: { // parentId가 없는 댓글은 대댓글이 아니므로 parentId 가 null인 글만 가져온다.
              [Op.eq]: null
            }
          },
          include: [
            {
              model: User, // 댓글 작성자를 알기위해 댓글을 작성한 사용자 정보를 가져온다.
              attributes: ['userid'], // User테이블에서 userid만 조회한다.
            },
            {
              model: Comment, // 댓글의 댓글(대댓글)을 가져오기 위한 댓글에 속한 댓글을 가져온다.
              include: {
                model: User, // 대댓글을 작성한 사용자의 정보를 가져온다.
                attributes: ['userid'], // User테이블에서 userid만 조회한다.
              }
            },
          ]
        },
      ],
      where: {
        Public: true // 공개된 게시물만 출력시킨다.
      },
      order: [
        ['createdAt', 'DESC'], // 글 작성 최신순
        [Comment, 'createdAt', 'DESC'], // 댓글 작성 최신순
        [Comment, Comment, 'createdAt', 'DESC'], // 대댓글 작성 최신순
      ],
    });        
    res.render('main', {
      title: 'NodeBird',
      twits: questions,  // 찾은 게시물들은 twits로 넣어준다
      loginUserId: req.session.passport ? req.session.passport.user : null // 현재 로그인한 유저 아이디를 세션에서가져와 view로 전달한다.
    });
  } catch (err) {
    console.error(err);
    next(err);
  }
}); 

router.get('/hashtag', async (req, res, next) => {
  const query = req.query.hashtag;
  if (!query) {
    return res.redirect('/');
  }
  try {
    const hashtag = await Hashtag.findOne({ where: { title: query } });
    let posts = [];
    if (hashtag) {
      posts = await hashtag.getPosts({ include: [{ model: User }] });
    }

    return res.render('main', {
      title: `${query} | NodeBird`,
      twits: posts,
    });
  } catch (error) {
    console.error(error);
    return next(error);
  }
});

router.get('/user/search', isLoggedIn, async (req, res) => {
  // 사용자가 입력한 검색어를 가져온다.
  const searchText = req.query.searchText;
  // where 조건에 넣어줄 데이터를 저장할 객체를 생성한다.
  const search = { };
  // 사용자가 입력한 검색어가 있으면 nick 컬럼을 기준으로 like검색을한다.
  if (searchText != null) {
    search.nick = {
      [Op.like]: '%' + searchText + '%'
    }
  }

  // 전체 사용자 정보를 데이터베이스에서 검색한다.
  const users = await User.findAll({
    attributes: {
      // createdAt, updatedAt 날짜 정보를 보기 좋게 dateformat 해서 가져온다.
      include: [
        [Sequelize.fn ("DATE_FORMAT", Sequelize.col("createdAt"), "%Y-%m-%d %H:%i:%s"), "createdAt"],
        [Sequelize.fn ("DATE_FORMAT", Sequelize.col("updatedAt"), "%Y-%m-%d %H:%i:%s"), "updatedAt"],
      ]
    },
    // 위에서 설정한 검색 객체를 where 조건에 넣는다.
    where: search
  });
  console.log(users);
  res.status(200).send(users);
  // res.render('user_search', { users: users, searchText: searchText });
});

router.get('/twit/search', isLoggedIn, async (req, res) => {
  // 사용자가 입력한 검색어를 가져온다.
  const searchText = req.query.searchText;
  // where 조건에 넣어줄 데이터를 저장할 객체를 생성한다.
  const search = { Public: true };  // 공개된 게시물만 출력시킨다.
  // 사용자가 입력한 검색어가 있으면 Title, Type, Publisher, Distributor 컬럼을 기준으로 like검색을 OR로 연결하여 검색한다.
  if (searchText != null) {
    search[Op.or] = [
      { Title: { [Op.like]: '%' + searchText + '%' } },
      { Type: { [Op.like]: '%' + searchText + '%' } },
      { Publisher: { [Op.like]: '%' + searchText + '%' } },
      { Distributor: { [Op.like]: '%' + searchText + '%' } },
    ];
  }

  const questions = await Question.findAll({
    include: {
      model: User,
    },
    // 위에서 설정한 검색 객체를 where 조건에 넣는다.
    where: search,
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
  });

  console.log(questions);
  res.status(200).send(questions);
  // res.render('twit_search', { twits: questions, searchText: searchText });
});


// 나의 저장 컨텐츠에서 검색하기 
router.get('/mytwit/search', isLoggedIn, async (req, res) => {
  const userId = req.session.passport.user;
  // 사용자가 입력한 검색어를 가져온다.
  const searchText = req.query.searchText;
  // 사용자가 입력한 검색어가 있으면 Title, Type, Publisher, Distributor 컬럼을 기준으로 like검색을 OR로 연결하여 검색한다.
  const offset = req.body.offset;
  const limit = req.body.limit;
  const sort_field = req.body.sort_field;
  const sort_rule = req.body.sort_rule;
  const type = req.body.type
  const mythema = req.body.mythema
  const search = {};
  if (searchText != null) {
    search[Op.or] = [
      { Title: { [Op.like]: '%' + searchText + '%' } },
      { Type: { [Op.like]: '%' + searchText + '%' } },
      { Publisher: { [Op.like]: '%' + searchText + '%' } },
      { Distributor: { [Op.like]: '%' + searchText + '%' } },
    ];
  }

  const posts = await Post.findAll({
    include: {
      model: User,
      attributes: ['id', 'nick'],
      where: {
        id: userId, // 로그인한 사용자의 컨텐츠만 가져오도록 조건절을 넣어준다.
      }
    },
    where: search,
    order: [[sort_field, sort_rule, type, mythema]], // 프론트로부터 정렬 정보를 받는다
    offset: offset,
    limit: limit,
  });
  console.log(posts);
  res.status(200).send(posts)
  // res.render('mytwit_search', { twits: posts, searchText: searchText });
});


// 트랜드 검색 
router.get('/trend/search', isLoggedIn, async (req, res) => {
  // 사용자가 입력한 검색어를 가져온다.
  const searchText = req.query.searchText;
  // where 조건에 넣어줄 데이터를 저장할 객체를 생성한다.
  const search = {};
  // 사용자가 입력한 검색어가 있으면 Title, Type, Publisher, Distributor 컬럼을 기준으로 like검색을 OR로 연결하여 검색한다.
  if (searchText != null) {
    search[Op.or] = [
      { Trend_Title: { [Op.like]: '%' + searchText + '%' } },
      { Trend_SubTitle: { [Op.like]: '%' + searchText + '%' } },
      { Trend_text: { [Op.like]: '%' + searchText + '%' } },
    ];
  }

  const posts = await Trend.findAll({
    include: {
      model: User,
    },
    // 위에서 설정한 검색 객체를 where 조건에 넣는다.
    where: search,
    order: [['createdAt', 'DESC']], // 최신순으로 가져오도록 정렬 조건을 준다.
  });

  console.log(posts);
  res.status(200).send(posts)
  // res.render('trend_search', { twits: posts, searchText: searchText });
});




module.exports = router;
