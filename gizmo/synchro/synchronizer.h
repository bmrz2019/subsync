#ifndef __SYNCHRONIZER_H__
#define __SYNCHRONIZER_H__

#include "text/words.h"
#include "math/line.h"
#include "math/linefinder.h"
#include <set>
#include <cmath>
#include <climits>


struct CorrelationStats
{
	bool     correlated;
	double   factor;
	unsigned points;
	float    maxDistance;
	Line     formula;

	CorrelationStats();
	std::string toString(
			const char *prefix="<CorrelationStats ",
			const char *suffix=">") const;
};


class Synchronizer
{
	public:
		typedef std::set<Word> Entrys;
		typedef std::set<float> Buckets;

	public:
		Synchronizer(
				float    windowSize     = HUGE_VALF,
				double   minCorrelation = 0.0,
				float    maxDistance    = HUGE_VALF,
				unsigned minPointsNo    = 0,
				float    minWordsSim    = 0.5);

		bool addSubWord(const Word &word);
		bool addRefWord(const Word &word);
		void addSubtitle(double startTime, double EndTime);

		CorrelationStats correlate() const;

		const Entrys &getSubs() const;
		const Entrys &getRefs() const;

		const Points &getAllPoints() const;
		Points getUsedPoints() const;

	private:
		unsigned countBuckets(const Points &pts, unsigned limit=UINT_MAX) const;

	private:
		Entrys m_subs;
		Entrys m_refs;
		Buckets m_buckets;

		LineFinder m_lineFinder;

		const float    m_windowSize;
		const double   m_minCorrelation;
		const float    m_maxDistanceSqr;
		const unsigned m_minPointsNo;
		const float    m_minWordsSim;
};

#endif
