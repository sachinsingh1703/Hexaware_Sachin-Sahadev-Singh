use careerhub;
/*
create table campanies(
companyid int primary key identity(101,1), 
companyname varchar(25),
location varchar(25));
*/
--exec sp_rename 'campanies' , 'companies';
/*
create table jobs(
jobid int primary key identity(11,1),
companyid int, constraint fk_company foreign key (companyid) references companies(companyid) on delete cascade,
jobtitle varchar(25),
jobdescription varchar(50),
joblocation varchar(25),
salary decimal(10,2),
jobtype varchar(25),
posteddate datetime default getdate());
*/
/*
create table applicants(
applicantid int primary key identity(25000,1),
firstname varchar(25),
lastname varchar(25),
email varchar(30),
phone varchar(13), constraint chk_phone check (phone like '[0,9]%'),
resume text
);
*/
/*
create table applications(
applicatioid int primary key identity(10021,1),
jobid int, constraint fk_jobs foreign key (jobid) references jobs(jobid),
applicantid int, constraint fk_applicant foreign key (applicantid) references applicants(applicantid),
applicationdate datetime default getdate(),
coverletter text);
*/
/*
INSERT INTO Companies (CompanyName, Location) VALUES 
('TechCorp', 'New York'),
('Innovate Ltd', 'San Francisco'),
('SoftSolutions', 'Chicago'),
('CodeCrafters', 'Los Angeles'),
('DataWorks', 'Houston'),
('NextGen Tech', 'Seattle'),
('AI Systems', 'Austin'),
('ByteWorks', 'Boston'),
('CloudSync', 'Denver'),
('QuantumSoft', 'Miami');

INSERT INTO Jobs (CompanyID, JobTitle, JobDescription, JobLocation, Salary, JobType) VALUES 
(101, 'Software Engineer', 'Develop and maintain software applications', 'New York', 85000.00, 'Full-time'),
(102, 'Data Analyst', 'Analyze data and generate reports', 'San Francisco', 72000.00, 'Full-time'),
(103, 'Web Developer', 'Build and maintain websites', 'Chicago', 68000.00, 'Contract'),
(101, 'Backend Developer', 'Develop scalable backend APIs', 'New York', 90000.00, 'Full-time'),
(105, 'Cybersecurity Specialist', 'Ensure security of digital assets', 'Houston', 88000.00, 'Part-time'),
(102, 'Business Analyst', 'Analyze and optimize business processes', 'San Francisco', 75000.00, 'Full-time'),
(104, 'Project Manager', 'Manage software development projects', 'Los Angeles', 95000.00, 'Full-time'),
(106, 'Machine Learning Engineer', 'Develop AI models', 'Austin', 100000.00, 'Full-time'),
(101, 'DevOps Engineer', 'Manage CI/CD pipelines', 'New York', 92000.00, 'Full-time'),
(103, 'Frontend Developer', 'Design user interfaces', 'Chicago', 70000.00, 'Contract');

INSERT INTO Applicants (FirstName, LastName, Email, Phone, Resume) VALUES 
('John', 'Doe', 'john.doe@email.com', '9876543210', 'Experienced software engineer.'),
('Alice', 'Smith', 'alice.smith@email.com', '9123456789', 'Certified data analyst.'),
('Bob', 'Johnson', 'bob.johnson@email.com', '9988776655', 'Skilled web developer.'),
('Emma', 'Williams', 'emma.williams@email.com', '9234567890', 'Project management professional.'),
('David', 'Brown', 'david.brown@email.com', '9345678901', 'Expert in cybersecurity.'),
('Sophia', 'Taylor', 'sophia.taylor@email.com', '9456789012', 'Passionate about data science.'),
('Michael', 'Anderson', 'michael.anderson@email.com', '9567890123', 'Full-stack developer.'),
('Emily', 'Harris', 'emily.harris@email.com', '9678901234', 'Product management expert.'),
('Daniel', 'Clark', 'daniel.clark@email.com', '9789012345', 'DevOps and cloud computing specialist.'),
('Olivia', 'Martinez', 'olivia.martinez@email.com', '9890123456', 'Aspiring AI researcher.');

INSERT INTO Applications (JobID, ApplicantID, CoverLetter) VALUES 
(11, 25000, 'I am passionate about software development and eager to contribute to your team.'),
(12, 25001, 'I love analyzing data and finding insights to drive business decisions.'),
(13, 25002, 'Building websites is my passion, and I am excited to apply for this role.'),
(14, 25003, 'I have a strong background in project management and leadership.'),
(15, 25004, 'Cybersecurity is my expertise, and I am eager to secure digital environments.'),
(11, 25005, 'Backend development excites me, and I have relevant experience in APIs.'),
(12, 25006, 'As a data scientist, I bring analytical skills and business acumen.'),
(13, 25007, 'My frontend development experience aligns perfectly with your job posting.'),
(11, 25008, 'DevOps automation is my strength, and I am eager to join your team.'),
(15, 25009, 'Artificial intelligence and machine learning are my fields of expertise.');
*/
--4
/*
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'careerhub')
BEGIN
    CREATE DATABASE careerhub;
    PRINT 'Database careerhub created successfully.';
END
ELSE
    PRINT 'Database already exists.';
*/
--5
/*
select apt.jobid,j.jobtitle, count(apt.applicantid) application_received
from jobs j
left join applications apt
on j.jobid = apt.jobid
group by apt.jobid, j.jobtitle;
*/

--6
/*
declare @minsal decimal(10,2) = 70000;
declare @maxsal decimal(10,2) = 100000;

select j.jobtitle, c.companyname, c.location, j.salary
from jobs j join companies c
on j.companyid = c.companyid
where j.salary between @minsal and @maxsal;
*/

--7
/*
declare @apli_id int = '25002';
select j.jobtitle, c.companyname, a.applicationdate
from jobs j 
join companies c on j.companyid = c.companyid
join applications a on j.jobid = a.jobid
where a.applicantid = @apli_id;
*/

--8
/*
select avg(salary) as avy_salary
from jobs 
where salary <> 0;
*/

--9
/*
select c.companyname, count(j.jobid) posted_count
from companies c
left join jobs j on c.companyid = j.companyid
group by c.companyname
order by posted_count desc;
*/

--10
/*
declare @pre_loc varchar(15) = 'San Francisco';
select a.applicantid, a.firstname, a.lastname, j.joblocation
from applicants a 
join applications apt on a.applicantid = apt.applicantid
join jobs j on apt.jobid = j.jobid
where j.joblocation = @pre_loc;
*/

--11
/*
select distinct(jobtitle), salary 
from jobs 
where salary between 60000 and 80000;
*/

--12
/*
select j.jobid, j.jobtitle
from jobs j left join applications a
on j.jobid = a.jobid
where a.applicantid is null;
*/

--13
/*
select a.applicantid, a.firstname, j.companyid, j.jobtitle
from applicants a 
left join applications apt on a.applicantid = apt.applicantid
left join jobs j on apt.jobid = j.jobid;
*/

--14
/*
select c.companyname, count(j.jobid) as cnt
from companies c
left join jobs j on c.companyid = j.companyid
group by c.companyname
order by cnt desc;
*/

--15
/*
select a.firstname, c.companyname, j.jobtitle
from applicants a 
left join applications apt on a.applicantid = apt.applicantid 
left join jobs j on apt.jobid = j.jobid 
left join companies c on j.companyid = c.companyid;
*/

--16
/*
select c.companyname, j.salary 
from companies c
join jobs j on c.companyid = j.companyid
where j.salary > (select avg(salary) from jobs);
*/

--17
/*
select a.firstname + ' ' + a.lastname as fullname,
j.joblocation
from applicants a 
left join applications apt on a.applicantid = apt.applicantid
left join jobs j on apt.jobid = j.jobid ;
*/

--18
/*
select jobid, jobtitle
from jobs 
where jobtitle in ('data analyst', 'engineer');
*/

--19
/*
select a.applicantid, a.firstname, j.jobtitle
from applicants a 
full outer join applications apt on a.applicantid = apt.applicantid
full outer join jobs j on apt.jobid = j.jobid;
*/
--20
/*
select a.applicantid, c.companyname, c.location
from applicants a 
join applications apt on a.applicantid = apt.applicantid
join jobs j on apt.jobid = j.jobid
cross join companies c
where c.location = 'san francisco';
*/
