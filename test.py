from data import db_session
from data.users import User

from data.jobs import Job, HHRU_CODE, SUPERJOB_CODE, FavouriteTable

user = User()
user.telegram_id = 1133234
user.specialization = "asdfasdf"
job = Job(job_id="12314124", source=HHRU_CODE)
job.job_id = "12314124"
job.source = HHRU_CODE
meta = FavouriteTable()
meta.user_id = 1
meta.job_id = 1
db_session.global_init("db/database.db")
db_sess = db_session.create_session()
db_sess.add(meta)
db_sess.add(job)
db_sess.add(user)
db_sess.commit()

