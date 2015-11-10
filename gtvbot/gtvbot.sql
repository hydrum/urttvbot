CREATE TABLE IF NOT EXISTS `betting` (
  `ID` text NOT NULL,
  `TeamA` text NOT NULL,
  `TeamB` text NOT NULL,
  `Draw` text NOT NULL,
  `Total` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `betting_host` (
  `ID` text NOT NULL,
  `host` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `gtv_new` (
  `ID` text NOT NULL,
  `TeamA` text NOT NULL,
  `TeamB` text NOT NULL,
  `Date` text NOT NULL,
  `Time` text NOT NULL,
  `League` text NOT NULL,
  `Type` text NOT NULL,
  `Who` text NOT NULL,
  `Server` text NOT NULL,
  `Public` varchar(3) NOT NULL DEFAULT 'no',
  `Done` varchar(3) NOT NULL DEFAULT 'no',
  `Score` text NOT NULL,
  `Demo` text NOT NULL,
  `Month` text NOT NULL,
  `Spam` text NOT NULL,
  `Shoutcast` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `status_new` (
  `Name` text NOT NULL,
  `Status` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `servers` (
  `ID` int(11) NOT NULL,
  `IP` text NOT NULL,
  `Admin` text NOT NULL,
  `Camera` text NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;