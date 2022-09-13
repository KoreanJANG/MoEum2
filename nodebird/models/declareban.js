const Sequelize = require('sequelize');

module.exports = class Declareban extends Sequelize.Model {
  static init(sequelize) {
    return super.init({      
        declaretext : {
        type: Sequelize.STRING(300),
        allowNull: true,
      },
        banid : {
        type: Sequelize.STRING(50),
        allowNull: true,
      },

    }, {
      sequelize,
      timestamps: true,
      underscored: false,
      modelName: 'Declareban',
      tableName: 'Declarebans',
      // 게시물은 실제 삭제하지 않고 deletedAt에 날짜를 넣다.
      paranoid: true,
      charset: 'utf8mb4',  // 이모티콘 가능 
      collate: 'utf8mb4_general_ci',
    });
  }

  static associate(db) {
    //신고차단은 유저에 속한다  
    db.Declareban.belongsTo(db.User, {
      foreignKey: 'userId' // FK 컬럼명
    }); 
    // 유저는 많은 신고차단을 가지고 있다  (일대다)
    db.User.hasMany(db.Declareban, {
      foreignKey: { // FK 설정
        name: 'userId', // FK 컬럼명
        allowNull: false // 신고차단은 반드시 유저아이디를 갖는다
      }
    });

    db.Declareban.belongsTo(db.Question, {
      foreignKey: 'declarequestionid' // FK 컬럼명
    }); 
    // 유저는 많은 신고차단을 가지고 있다  (일대다)
    db.Question.hasMany(db.Declareban, {
      foreignKey: { // FK 설정
        name: 'declarequestionid', // FK 컬럼명
        allowNull: true // 신고차단은 질문이 아닐수도 있다 
      }
    });

    db.Declareban.belongsTo(db.Comment, {
      foreignKey: 'declarecommentid' // FK 컬럼명
    }); 
    // 유저는 많은 신고차단을 가지고 있다  (일대다)
    db.Comment.hasMany(db.Declareban, {
      foreignKey: { // FK 설정
        name: 'declarecommentid', // FK 컬럼명
        allowNull: true // 신고차단은 댓글이 아닐수도 있다 
      }
    });

    db.Declareban.belongsTo(db.Trendcomment, {
      foreignKey: 'declaretrendcommentid' // FK 컬럼명
    }); 
    // 유저는 많은 신고차단을 가지고 있다  (일대다)
    db.Trendcomment.hasMany(db.Declareban, {
      foreignKey: { // FK 설정
        name: 'declaretrendcommentid', // FK 컬럼명
        allowNull: true // 신고차단은 트랜드 댓글이 아닐수도 있다 
      }
    });
 }
};
