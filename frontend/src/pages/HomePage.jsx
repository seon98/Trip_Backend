import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Spinner, Alert } from 'react-bootstrap';

const API_URL = 'https://tteonabom-backend.onrender.com/accommodations/';

function HomePage() {
  const [accommodations, setAccommodations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(API_URL)
      .then(response => {
        if (!response.ok) { throw new Error('Network response was not ok'); }
        return response.json();
      })
      .then(data => {
        setAccommodations(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching accommodations:", error);
        setError("데이터를 불러오는 데 실패했습니다. 잠시 후 다시 시도해주세요.");
        setLoading(false);
      });
  }, []);

  if (loading) return <Container className="text-center mt-5"><Spinner animation="border" /></Container>;
  if (error) return <Container className="mt-4"><Alert variant="danger">{error}</Alert></Container>;

  return (
    <Container>
      <h2 className="my-4">추천 숙소</h2>
      <Row>
        {accommodations.length > 0 ? accommodations.map(acc => (
          <Col key={acc.id} md={4} className="mb-4">
            <Card>
              <Card.Img variant="top" src={`https://picsum.photos/seed/${acc.id}/400/250`} />
              <Card.Body>
                <Card.Title>{acc.name}</Card.Title>
                <Card.Text><strong>위치:</strong> {acc.location}</Card.Text>
                <Card.Footer className="text-muted">등록자: {acc.owner.email}</Card.Footer>
              </Card.Body>
            </Card>
          </Col>
        )) : <p>등록된 숙소가 없습니다.</p>}
      </Row>
    </Container>
  );
}

export default HomePage;
