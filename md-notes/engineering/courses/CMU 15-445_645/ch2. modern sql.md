# chap 2: modern sql
[lec](https://15445.courses.cs.cmu.edu/spring2024/notes/02-modernsql.pdf)
- sql is based on bags - multisets (allow duplicates) not sets (no duplicates)
- aggregate functions
	- `AVG`, `MIN`, `MAX`, `SUM`, `COUNT` -> used in `SELECT` output list
	- `COUNT`, `SUM`, `AVG` support `DISTINCT` modifier
	```sql
SELECT COUNT(DISTINCT login)
FROM student WHERE login LIKE '%@cs'
```
- `GROUP BY` projects tuples into subsets and calculate aggregates on each subset
	```sql
SELECT AVG(s.gpa), e.cid
FROM enrolled AS e JOIN student AS s
ON e.sid = s.sid
GROUP BY e.cid
```
- `HAVING` filters results based on aggregation computation, similar to `WHERE` for `GROUP BY` clause
	```sql
SELECT AVG(s.gpa) AS avg_gpa, e.cid
FROM enrolled AS e, student AS s
WHERE e.sid = s.sid
GROUP BY e.cid
HAVING AVG(s.gpa) > 3.9; -- not HAVING avg_gpa > 3.9;
```
- `LIKE` for string matching
	- '%' matches any substring (including empty string)
	- '\_' matches any character
- string operations
- date/time operations
- output direction
	- store results in another (temporary) table: `INSERT`
- output control
	- `ORDER BY` (ASC|DESC)
	- `FETCH` with offset
- window functions
	[ranking window function](https://datalemur.com/sql-tutorial/sql-rank-dense_rank-row_number-window-function)
	- perform sliding calculation across a set of tuples, like an aggregation but not grouping
	- steps:
		- partition data
		- sorts each partition
		- create a window and compute an answer for each window
		```sql
SELECT 
  RANK() / DENSE_RANK() / ROW_NUMBER() OVER ( -- Compulsory expression
    PARTITION BY partitioning_expression -- Optional expression
    ORDER BY order_expression) -- Compulsory expression
FROM table_name;
```
	- functions:
		- `ROW_NUMBER`: the number of current row -> assign unique sequential number
		- `RANK`: the order position of current row -> handle tied values by assign same rank number, and skip sequential ranks
		- `DENSE_RANK`: same as `RANK` but not skipping sequential ranks
	- grouping:
		- `OVER`: clause specifies how to grouping tuples together
		- `PARTITION BY`: specify group
		```sql
SELECT * FROM (
SELECT *, RANK() OVER (PARTITION BY cid
ORDER BY grade ASC) AS rank
FROM enrolled) AS ranking
WHERE ranking.rank = 2;
```
- nested queries
	- invoke queries inside of other queries -> difficult to optimize
	```sql
SELECT name FROM student
WHERE sid IN (
SELECT sid FROM enrolled
WHERE cid = '15-445'
);
```
- lateral join
	- `LATERAL` allows a nested query to reference attributes in other nested queries that precede it
	```sql
SELECT * FROM course AS c -- for each course
LATERAL (SELECT COUNT(*) AS cnt FROM enrolled -- compute the number of enrolled students
WHERE enrolled.cid = c.cid) AS t1,
LATERAL (SELECT AVG(gpa) AS avg FROM student AS s -- compute the average gpa of enrolled students
JOIN enrolled AS e ON s.sid = e.sid
WHERE e.cid = c.cid) AS t2;
```
- table expression
	- an alternative to windows/nested queries when writing complex queries (though as a temporary table is scoped for a single query) -> write auxiliary statements