Sensitive data are usually protected by access controls which allow
subjects (users, programs) specific types of access (e.g. read, write,
modify) to constrain the viewing or extraction of information
(confidentiality), or the ways in which it may be changed
(Integrity), or both.

Internet Users are familiar with how browsing behaviour is
tracked and consolidated to provide a profile of 'interests'
which are then used to provide targeted advertising. This
'linkage' of information may be helpful (if you enjoy
advertising!) or regarded as a violation of privacy.

The problem of inferring sensitive information from data
fragments or statistics which are otherwise not sensitive is a
common concern of database designers. For example, queries
against public census information or customer databases that
provide aggregated statistics may be contrived to intersect in
such a way that they reveal information about single identities
in the system.

dbinfer is a progam which supports inference experiments by
providing access to a small database of 'Students and Exam
Grades'. Program features include command-line and API
interfaces, statistical queries, and pre and post query
inference management policies.
