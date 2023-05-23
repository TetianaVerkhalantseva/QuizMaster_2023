from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy.orm import relationship, sessionmaker

from config import DevelopmentConfig


engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
base = declarative_base()


class User(base, UserMixin):

    def set_info(self, **kwargs):
        self.user_info = kwargs

    def __getitem__(self, item):
        return None if not hasattr(self, 'user_info') or item not in self.user_info else self.user_info[item]

    __tablename__ = 'bruker'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50), nullable=False, unique=True)
    passord = Column(String(102), nullable=False)
    fornavn = Column(String(50), nullable=True)
    etternavn = Column(String(50), nullable=True)

    admin = Column(Boolean, nullable=False)
    student = Column(Boolean, nullable=False)


class Quiz(base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True, autoincrement=True)
    navn = Column(String(50), nullable=False)
    beskrivelse = Column(Text(1000), nullable=True)
    admin_id = Column(Integer, ForeignKey('bruker.id'), nullable=True)
    admin = relationship('User')


class QuestionCategory(base):
    __tablename__ = 'spørsmålskategori'
    id = Column(Integer, primary_key=True, autoincrement=True)
    navn = Column(String(50), nullable=False)


class Question(base):
    __tablename__ = 'spørsmål'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spørsmål = Column(Text(500), nullable=False)
    kategori_id = Column(Integer, ForeignKey('spørsmålskategori.id'), nullable=False)
    admin_id = Column(Integer, ForeignKey('bruker.id'), nullable=False)
    riktig_svarpoeng = Column(Float, nullable=False)

    kategori = relationship('QuestionCategory')
    admin = relationship('User')
    answer_options = relationship('AnswerOption', back_populates='spørsmål')


class AnswerOption(base):
    __tablename__ = 'svarmulighet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    svar = Column(Text(500), nullable=False)
    korrekt = Column(Boolean, nullable=False)
    spørsmål_id = Column(Integer, ForeignKey('spørsmål.id'), nullable=False)
    spørsmål = relationship('Question')


class QuestionHasQuiz(base):
    __tablename__ = 'spørsmål_har_quiz'
    id = Column(Integer, primary_key=True, autoincrement=True)
    spørsmål_id = Column(Integer, ForeignKey('spørsmål.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    spørsmål = relationship('Question')
    quiz = relationship('Quiz')


class QuizSession(base):
    __tablename__ = 'quiz_sesjon'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('bruker.id'), nullable=False)
    godkjent = Column(Boolean, nullable=True)


class QuizSessionAnswer(base):
    __tablename__ = 'quiz_sesjon_svar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_sesjon_id = Column(Integer, ForeignKey('quiz_sesjon.id'), nullable=False)
    spørsmål_id = Column(Integer, ForeignKey('spørsmål.id'), nullable=False)
    svarmulighet_id = Column(Integer, ForeignKey('svarmulighet.id'), nullable=True)
    tekstsvar = Column(Text(1000), nullable=True)
    godkjent = Column(Boolean, nullable=True)


class QuizComment(base):
    __tablename__ = 'quiz_kommentar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_sesjon_id = Column(Integer, ForeignKey('quiz_sesjon.id'), nullable=False)
    bruker_id = Column(Integer, ForeignKey('bruker.id'), nullable=True)
    tekst = Column(Text(1000), nullable=False)


class AnswerComment(base):
    __tablename__ = 'svar_kommentar'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_sesjon_svar_id = Column(Integer, ForeignKey('quiz_sesjon_svar.id'), nullable=False)
    bruker_id = Column(Integer, ForeignKey('bruker.id'), nullable=True)
    tekst = Column(Text(1000), nullable=False)


base.metadata.create_all(engine)

db_session = sessionmaker()(bind=engine)
