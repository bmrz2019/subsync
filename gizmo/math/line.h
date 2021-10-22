#ifndef __LINE_H__
#define __LINE_H__

#include "point.h"
#include <cstddef>
#include <string>


class Line
{
	public:
		float a, b;

	public:
		Line();
		Line(float a, float b);
		Line(const Point &p1, const Point &p2);

		inline float getX(float y) const { return (y-b) / a; }
		inline float getY(float x) const { return a*x + b; }

		double interpolate(const Points &points);

		float getDistanceSqr(const Point &point) const;
		float getDistance(const Point &point) const;

		Points getPointsInLine(const Points &points) const;
		Points getPointsInLine(const Points &points, float maxDistSqr) const;

		size_t countPointsInLine(const Points &points) const;
		size_t countPointsInLine(const Points &points, float maxDistSqr) const;

		float findFurthestPoint(const Points &points) const;
		float removeFurthestPoint(Points &points) const;

		std::string toString() const;
};

#endif
