// =====================================================================
// DAY 4 - C++ review
// Rules: no autocomplete, no docs, no AI. Narrate out loud as you code.
//
//   g++ -std=c++17 -Wall -Wextra day4.cpp -o day4 && ./day4
//
// Target: all PASS in under 2 hours.
//
// This rebuilds your drone sensor sim from scratch, plus the ring buffer.
// Bryan Ling is a Staff Vision Engineer whose top listed skill is C++,
// and he is your first interview. Every keyword here should be one you
// can explain, not just type.
// =====================================================================

#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <map>
#include <cmath>
#include <sstream>
#include <algorithm>
#include <stdexcept>
#include <optional>

// =====================================================================
// PART A: A plain class  (target 20 min)
// =====================================================================
//
// Reading holds one measurement: a timestamp (double) and a value (double).
//
// Build it with both values. Expose them read-only through getters.
// Provide a method that reports whether the value sits inside a given
// inclusive range.
//
// Use a member initializer list in the constructor. Mark every method
// that does not modify the object as const.

class Reading {
    double ts_{};
    double value_{};
public:

    // Default constructor
    Reading() {}
    // Paramaterized constructor
    Reading(double t, double v): ts_{t}, value_{v}{}


    double ts() const{
        return ts_;
    }
    double value() const{
        return value_;
    }

    bool inRange(double low, double high) const{
        return low<=value_ && high>= value_;
    }
};


// =====================================================================
// PART B: Abstract base + polymorphism  (target 35 min)
// =====================================================================
//
// SensorBase is abstract. It cannot be instantiated. Every sensor has a
// name, can produce a reading given a tick number, and reports whether a
// value is anomalous for that sensor type.
//
//   name()          -> the sensor's type name
//   read(tick)       -> a double, the value at that tick
//   isAnomalous(v)   -> whether v is outside this sensor's normal band
//
// name() and read() differ per sensor, so they are pure virtual.
// isAnomalous() has a default implementation using a low/high band stored
// in the base -- derived classes may override it.
//
// Think hard about the destructor. There is exactly one thing you must do
// to a base class destructor when objects are deleted through a base
// pointer, and getting it wrong leaks.

class SensorBase {
    // TODO: store the band. Derived classes need to read it; nothing outside
    // the hierarchy should.
public:
    // The tests construct a derived class that calls SensorBase(lo, hi),
    // so keep this signature.
    SensorBase(double lo, double hi);
    virtual ~SensorBase();
    virtual std::string name() const = 0;
    virtual double read(int tick) const = 0;
    virtual bool isAnomalous(double v) const;
};

// Imu:          band [-2.0, 2.0],   read(tick) returns 0.5 * tick
// Ultrasonic:   band [0.0, 400.0],  read(tick) returns 10.0 * tick
// Temperature:  band [-40.0, 85.0], read(tick) returns 20.0 + tick
//               Temperature OVERRIDES isAnomalous: it is anomalous if the
//               value is outside the band OR is exactly 0.0 (a common
//               failure mode for a disconnected thermocouple).

class Imu : public SensorBase {
    // TODO
};

class Ultrasonic : public SensorBase {
    // TODO
};

class Temperature : public SensorBase {
    // TODO
};


// Given a collection of sensors and a tick, return the name of every
// sensor reporting an anomalous reading at that tick, in order.
//
// The parameter type matters: you are not copying the sensors, and you
// are not modifying them.
std::vector<std::string> anomalousAt(
        const std::vector<std::unique_ptr<SensorBase>>& sensors, int tick);


// =====================================================================
// PART C: Ring buffer  (target 30 min)
// =====================================================================
//
// Fixed-capacity buffer. When full, a push overwrites the OLDEST value.
//
//   RingBuffer(capacity)  -- an invalid capacity is an error
//   push(value)           -- reports what it evicted, if anything
//   size(), isFull(), empty()
//   toVector()            -- oldest first
//   mean()                -- of what it currently holds
//
// Use a std::vector<double> sized once in the constructor, plus an index.
// Do not push_back or erase. Nothing may shift.
//
// push must report "evicted X" or "evicted nothing" -- pick a return type
// that can express both without a sentinel value.

// The tests call these, so keep the names:
//   RingBuffer(capacity)
//   push(value)
//   size()
//   isFull()
//   empty()
//   toVector()
//   mean()
//
// Everything else -- parameter types, return types, which members you store --
// is yours to decide. Two of these have to express "there is no answer"
// without reserving a magic value; C++17 has a type for that.

// TODO: class RingBuffer
#include <vector>
#include <cstdint>
class RingBuffer{

std::uint64_t capacity{};
std::vector<double> buffer{};
std::uint64_t start{};
std::uint64_t n{};
double total_sum{};



public:

    RingBuffer(int size): capacity(size), buffer(size){
        if(size<=0){
            throw std::invalid_argument("Capacity must be >=1");
        }
    }
    std::optional<double> push(double value){
        double prev_value = buffer[(n + start) % capacity];
        buffer[(n + start) % capacity] = value;
        if(n< capacity){
            ++n;
            total_sum += value;
            return std::nullopt;
        }
        else{
            total_sum -= prev_value;
            total_sum += value;
            ++start;
            return prev_value;
        }
    }

    std::size_t size() const{
        return static_cast<std::size_t>(n);
    }

    bool isFull() const{
        return n == capacity;
    }
    bool empty() const{
        return n==0;
    }
    std::optional<double> mean() const{
        if(n==0){
            return std::nullopt;
        }

        return total_sum / n;
    }
    std::vector<double> toVector() const{
        if(n < capacity){
            std::vector<double> result;
            for(int i = 0; i<n; ++i){
                result.push_back(buffer[i]);
            }
            return result;
        }
        else{
            std::vector<double> result;
            for(int i = (start % capacity); i<capacity; ++i){
                result.push_back(buffer[i]);
            }
           
            for(int i = 0; i< (start% capacity); ++i){
                result.push_back(buffer[i]);
            }
            return result;
            
        }
    }






};

// =====================================================================
// PART D: STL + parsing  (target 25 min)
// =====================================================================

// Split a string on a delimiter. Empty fields are kept.
//   "a,b,,c" , ','  ->  {"a", "b", "", "c"}
//   ""       , ','  ->  {""}
std::vector<std::string> split(const std::string& s, char delim);


// Each line is "station,value". Group the values by station and return
// {station: mean}. Skip any line that does not have exactly two fields
// or whose value does not parse as a number.
std::map<std::string, double> meanByStation(const std::vector<std::string>& lines);


// Return the k largest values, descending. If k exceeds the input size,
// return everything sorted descending. Do not modify the caller's vector
// -- note what the parameter type has to be for that to hold.
std::vector<double> topK(std::vector<double> values, std::size_t k);


// =====================================================================
// ========================= TESTS (don't edit) ========================
// =====================================================================

static int g_pass = 0, g_fail = 0;

static void check(bool cond, const std::string& label) {
    if (cond) { std::cout << "PASS  " << label << "\n"; ++g_pass; }
    else      { std::cout << "FAIL  " << label << "\n"; ++g_fail; }
}

static bool close(double a, double b) { return std::fabs(a - b) < 1e-9; }

// Tracks whether derived destructors actually run.
static int g_destroyed = 0;
struct DtorProbe : public SensorBase {
    DtorProbe() : SensorBase(0.0, 1.0) {}
    ~DtorProbe() override { ++g_destroyed; }
    std::string name() const override { return "probe"; }
    double read(int) const override { return 0.0; }
};

int main() {
    // ---- Part A ----
    {
        Reading r(1.5, 12.25);
        check(close(r.ts(), 1.5) && close(r.value(), 12.25), "Reading stores ts and value");
        check(r.inRange(12.0, 13.0), "inRange inside");
        check(!r.inRange(0.0, 12.0), "inRange above");
        check(r.inRange(12.25, 12.25), "inRange is inclusive");
        const Reading cr(0.0, 5.0);
        check(close(cr.value(), 5.0), "getters are const-callable");
    }

    // ---- Part B ----
    {
        Imu imu;
        Ultrasonic us;
        Temperature t;
        check(imu.name() == "Imu", "Imu::name");
        check(us.name() == "Ultrasonic", "Ultrasonic::name");
        check(t.name() == "Temperature", "Temperature::name");
        check(close(imu.read(4), 2.0), "Imu::read");
        check(close(us.read(3), 30.0), "Ultrasonic::read");
        check(close(t.read(5), 25.0), "Temperature::read");

        check(!imu.isAnomalous(1.0) && imu.isAnomalous(2.5), "Imu band");
        check(!us.isAnomalous(399.0) && us.isAnomalous(401.0), "Ultrasonic band");
        check(t.isAnomalous(0.0), "Temperature overrides: 0.0 is anomalous");
        check(!t.isAnomalous(20.0), "Temperature normal value");
        check(t.isAnomalous(200.0), "Temperature out of band");

        // polymorphism through a base pointer
        SensorBase* p = &imu;
        check(p->name() == "Imu", "virtual dispatch through base pointer");

        std::vector<std::unique_ptr<SensorBase>> sensors;
        sensors.push_back(std::make_unique<Imu>());
        sensors.push_back(std::make_unique<Ultrasonic>());
        sensors.push_back(std::make_unique<Temperature>());

        auto a0 = anomalousAt(sensors, 0);
        check(a0.empty(), "tick 0: nothing anomalous");

        auto a10 = anomalousAt(sensors, 10);
        check(a10.size() == 1 && a10[0] == "Imu", "tick 10: Imu at 5.0 is out of band");

        auto a50 = anomalousAt(sensors, 50);
        check(a50.size() == 2 && a50[0] == "Imu" && a50[1] == "Ultrasonic",
              "tick 50: Imu and Ultrasonic out, Temperature still fine");

        auto a100 = anomalousAt(sensors, 100);
        check(a100.size() == 3, "tick 100: all three out of band");

        // virtual destructor
        g_destroyed = 0;
        {
            std::unique_ptr<SensorBase> up = std::make_unique<DtorProbe>();
        }
        check(g_destroyed == 1, "derived dtor runs through a base pointer");
    }

    // ---- Part C ----
    {
        bool threw = false;
        try { RingBuffer bad(0); } catch (const std::exception&) { threw = true; }
        check(threw, "capacity 0 throws");

        RingBuffer rb(3);
        check(rb.size() == 0 && rb.empty() && !rb.isFull(), "starts empty");
        check(!rb.mean().has_value(), "mean of empty has no value");
        check(!rb.push(1.0).has_value(), "push into space evicts nothing");
        rb.push(2.0);
        rb.push(3.0);
        check(rb.isFull() && rb.size() == 3, "full at capacity");
        check(rb.toVector() == std::vector<double>({1.0, 2.0, 3.0}), "toVector oldest first");
        check(rb.mean().has_value() && close(*rb.mean(), 2.0), "mean");

        auto ev = rb.push(4.0);
        check(ev.has_value() && close(*ev, 1.0), "push evicts the oldest");
        check(rb.toVector() == std::vector<double>({2.0, 3.0, 4.0}), "wrapped correctly");
        rb.push(5.0);
        check(rb.toVector() == std::vector<double>({3.0, 4.0, 5.0}), "wrapped twice");
        check(rb.size() == 3, "size never exceeds capacity");
    }

    // ---- Part D ----
    {
        check(split("a,b,,c", ',') == std::vector<std::string>({"a","b","","c"}), "split keeps empties");
        check(split("", ',') == std::vector<std::string>({""}), "split of empty string");
        check(split("solo", ',') == std::vector<std::string>({"solo"}), "split with no delim");

        std::vector<std::string> lines = {
            "ST1,10", "ST2,4", "ST1,12", "garbage", "ST2,abc", "ST3,7,8"
        };
        auto m = meanByStation(lines);
        check(m.size() == 2, "bad lines skipped");
        check(m.count("ST1") && close(m["ST1"], 11.0), "ST1 mean");
        check(m.count("ST2") && close(m["ST2"], 4.0), "ST2 mean");

        std::vector<double> v = {5.2, 3.1, 4.8, 2.9, 6.0};
        auto t2 = topK(v, 2);
        check(t2 == std::vector<double>({6.0, 5.2}), "topK");
        check(v.size() == 5 && close(v[0], 5.2), "topK did not modify the caller's vector");
        check(topK(v, 99).size() == 5, "k larger than input");
        check(topK(v, 0).empty(), "k == 0");
    }

    std::cout << "\n" << g_pass << "/" << (g_pass + g_fail) << " passed\n";
    return g_fail == 0 ? 0 : 1;
}